import esprima
import re

from decode_reimpls import *
from visitors import *

def dropper_stage1_deobfuscate(code: str)  -> str:
    ast = esprima.parse(code)

    # Try to get the inner IIFE body node, expecting the format:
    """
        global['_V'] = '5-143';
        global['r'] = require;
        if (typeof module === 'object') global['m'] = module;
        (function() {
            /* stage1 inner IIFE code */
    })()
    """

    iife_nodes = [node for node in ast.body if node.type == 'ExpressionStatement' and node.expression.type == 'CallExpression' and node.expression.callee.type == 'FunctionExpression']
    assert len(iife_nodes) == 1, "stage1 obfuscation should have a single Immediately-Invoked-Function-Expression"
    iife_expr_body = iife_nodes[0].expression.callee.body

    # Try to get the decode function (& literals). We are expecting something like:
    """
        var Klu = '',
            QcU = 794 - 783;

        function Onn(d) {
            var w = 1019633;
            var c = d.length;
            var t = [];
            for (var n = 0; n < c; n++) {
                t[n] = d.charAt(n)
            };
            for (var n = 0; n < c; n++) {
                var e = w * (n + 82) + (w % 49761);
                var b = w * (n + 575) + (w % 41455);
                var g = e % c;
                var p = b % c;
                var o = t[g];
                t[g] = t[p];
                t[p] = o;
                w = (e + b) % 1671836;
            };
            return t.join('')
        };
        var ypw = Onn('wgnnsruxjouobcvhfroktztmseayqlticcdrp').substr(0, QcU);
    """
    iife_function_decls = [node for node in iife_expr_body.body if node.type == "FunctionDeclaration"]
    assert len(iife_function_decls) == 1, "stage1 obfuscation should have a single function decl (decode function) in the IIFE"
    decode1_function_decl = iife_function_decls[0]

    # Collect the randomized decode1 constants, as they are randomized for each sample/version of the dropper.
    collector = IntegerLiteralCollector()
    collector.visit(decode1_function_decl)
    decode1_constants = collector.literals

    # Collect the calls to the decode1 function
    collector = CallExpressionCollector(decode1_function_decl.id.name)
    collector.visit(iife_expr_body)
    decode1_calls = collector.call_nodes

    # Now try to get the decode2 function.
    # We are expecting this to be in the form of:
    #     var yRJ = <some large string literal>;
    #     var cNk = MyR(qyM, Onn(yRJ));
    # where `Onn` is the stage1 decode1 function.

    # First find the var holding decode2 code (`yRJ` in the example above)
    decode2_var = [call.arguments[0].name for call in decode1_calls if len(call.arguments) == 1 and call.arguments[0].type == 'Identifier'][0]
    # print(f"decode2_var:{decode2_var}")

    # Then find the decode2 raw literal value
    collector = VariableDeclaratorLiteralCollector()
    collector.visit(iife_expr_body)
    iife_var_decl_literals = collector.literals
    assert decode2_var in collector.literals, "stage1 must have second decode function literal"
    decode2_raw_literal = collector.literals[decode2_var]
    # print(decode2_raw_literal)

    # Decode decode2 with decode1
    decode2_clean_literal = stage1_decode1(decode2_raw_literal, decode1_constants)
    # print(decode2_clean_literal)

    # Get decode2 as a valid function (required for parsing w/ esprima as it has a "return" statement)
    decode2_function_str = f"function foo(){{{decode2_clean_literal}}}"
    # print(decode2_function_str)

    # Get decode2 constants
    decode2_raw_ast = esprima.parse(decode2_function_str)
    collector = IntegerLiteralCollector()
    collector.visit(decode2_raw_ast)
    decode2_constants = collector.literals
    # print(decode2_constants)

    # print(decode1_calls[-1])

    stage2_decode_call = decode1_calls[-1]
    assert len(stage2_decode_call.arguments) == 1, "stage1 final decode call should have 1 argument"
    assert stage2_decode_call.arguments[0].type == "Literal", "stage1 final decode call argument should be literal"
    stage2_payload_raw = stage2_decode_call.arguments[0].value

    stage2_payload_decoded1 = stage1_decode1(stage2_payload_raw, decode1_constants)
    stage2_payload_decoded2 = stage1_decode2(stage2_payload_decoded1, decode2_constants)
    # print(stage2_payload_decoded2)


    stage2_payload_as_iife = f"(function(){{{stage2_payload_decoded2}}})()"

    return stage2_payload_as_iife

def dropper_stage2_deobfucsate(code: str) -> str:
    ast = esprima.parse(code)
    # print(ast)

    iife_body = ast.body[0].expression.callee.body
    # print(iife_body)

    assert iife_body.body[0].type == "VariableDeclaration" and iife_body.body[0].declarations[0].init.type == "CallExpression", "stage2 should start with call to stage2_decode_identifiers"
    encoded_ids_var_name = iife_body.body[0].declarations[0].id.name
    decode_identifiers_function_name = iife_body.body[0].declarations[0].init.callee.name
    decode_identifiers_literal = iife_body.body[0].declarations[0].init.arguments[0].value
    decode_identifiers_key = iife_body.body[0].declarations[0].init.arguments[1].value

    # Get the function decl
    decode_identifiers_decl = [node for node in iife_body.body if node.type == "FunctionDeclaration" and node.id.name == decode_identifiers_function_name][0]

    # Collect the randomized decode constants
    collector = IntegerLiteralCollector()
    collector.visit(decode_identifiers_decl)
    decode_identifiers_constants = collector.literals
    # print(decode_identifiers_constants)

    # Decode the identifiers
    decoded_identifiers = stage2_decode_identifiers(decode_identifiers_literal, decode_identifiers_key, decode_identifiers_constants)
    # print(decoded_identifiers)

    # Unfortunately, esprima-python cannot properly handle MemberExpression nodes in the Visitor(/transformer),
    # so we do some ugly find/replace hacks here.
    cleaned_code = code
    for i in range(len(decoded_identifiers)):
        member_expr = f"{encoded_ids_var_name}[{i}]"
        inlined_expr = f"'{decoded_identifiers[i]}'"
        cleaned_code = cleaned_code.replace(member_expr, inlined_expr)

    cleaned_code = re.sub(r'var .*;function.{1,16}\{.*\.join\(.\).split\(.\)}', '', cleaned_code)

    return cleaned_code
