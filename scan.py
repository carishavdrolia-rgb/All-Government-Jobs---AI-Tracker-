import json, re, os, ssl, datetime, concurrent.futures as cf
from urllib.request import Request, urlopen
from urllib.parse import urljoin

LINKS = [
["Regulators","RBI Grade B","https://opportunities.rbi.org.in/scripts/vacancies.aspx"],
["Regulators","SEBI Grade A","https://www.sebi.gov.in/sebiweb/about/AboutAction.do?doVacancies=yes"],
["Regulators","PFRDA Grade A","https://pfrda.org.in/get-to-know/careers/vacancies"],
["Regulators","IRDAI Grade A (careers section)","https://irdai.gov.in"],
["Regulators","NPS Trust","https://npstrust.org.in/career-vacancies"],
["UPSC / SSC / IAF","UPSC Recruitment","https://www.upsc.gov.in/recruitment/recruitmentadvertisement"],
["UPSC / SSC / IAF","Indian Air Force (AFCAT)","https://afcat.edcil.co.in/"],
["UPSC / SSC / IAF","SSC CGL","https://ssc.gov.in/for-candidates/cgl-exam/xsd91hjkshdk92xk"],
["Financial Institutions","NABARD","https://www.nabard.org/careers-notices1.aspx?cid=693&id=26"],
["Financial Institutions","SIDBI","https://www.sidbi.in/en/careers"],
["Financial Institutions","EXIM Bank","https://www.eximbankindia.in/careers"],
["Financial Institutions","NHB","https://www.nhb.org.in/oppurtunitiesnhb/"],
["Financial Institutions","NaBFID / IIFCL","https://nabfid.org/en/careers"],
["Financial Institutions","IFCI","https://www.ifciltd.com/career"],
["Maharatna PSU","IOCL","https://iocl.com/latest-job-opening"],
["Maharatna PSU","Powergrid","https://www.powergrid.in/en/job-opportunities"],
["Maharatna PSU","SAIL","https://sailcareers.com/Archive.aspx?Section=Jobs"],
["Maharatna PSU","BHEL","https://careers.bhel.in/index.jsp#openings"],
["Maharatna PSU","Coal India","https://www.coalindia.in/career-cil/jobs-coal-india/"],
["Maharatna PSU","BPCL","https://www.bharatpetroleum.in/careers/job-openings"],
["Maharatna PSU","HPCL","https://www.hindustanpetroleum.com/job-openings"],
["Maharatna PSU","GAIL","https://www.gailonline.com/Vacancies.html"],
["Maharatna PSU","NTPC","https://careers.ntpc.co.in/recruitment/"],
["Maharatna PSU","ONGC","https://ongcindia.com/web/eng/career/recruitment-notice"],
["Maharatna PSU","HAL","https://hal-india.co.in/career"],
["Maharatna PSU","PFC","https://pfcindia.co.in/en/data/careers/jobs-on-offer"],
["Maharatna PSU","REC","https://recindia.nic.in/careers"],
["Maharatna PSU","Oil India","https://www.oil-india.com/advertisement-list"],
["Other PSU","NHPC","https://www.nhpcindia.com/welcome/job.html"],
["Other PSU","THDC","https://www.thdc.co.in/en/career/new-job-opening"],
["Other PSU","NPCIL","https://www.npcilcareers.co.in/MainSiten/DefaultInfo.aspx"],
["Other PSU","IRCTC","https://www.irctc.com/new-openings.php"],
["Other PSU","FCI","https://fci.gov.in/recruitment"],
["Other PSU","BEL","https://bel-india.in/job-notifications/"],
["Other PSU","NMDC","https://www.nmdc.co.in/careers"],
["Other PSU","NALCO","https://nalcoindia.com/careers"],
["Other PSU","NBCC","https://www.nbccindia.in/webEnglish/jobs"],
["Other PSU","RVNL","https://rvnl.org/job"],
["Other PSU","IRCON","https://ircon.org/career-ircon"],
["Other PSU","RITES","https://rites.com/career"],
["Other PSU","RailTel","https://www.railtel.in/careers.html"],
["Other PSU","Engineers India (EIL)","https://engineersindia.com/applying-to-eil"],
["Other PSU","SJVN","https://sjvn.nic.in/current-jobs"],
["Other PSU","Mazagon Dock","https://mazagondock.in/English/career/Career-Executives"],
["Other PSU","NLC India","https://www.nlcindia.in/website/en/careers/jobs/currentopenings.html"],
["Other PSU","Shipping Corp of India","https://www.shipindia.com/page/career"],
["Other PSU","RCFL","https://www.rcfltd.com/hr-recruitment"],
["Other PSU","NFL","https://careers.nfl.co.in/"],
["Other PSU","SECI","https://www.seci.co.in/jobs"],
["Other PSU","AAI","https://www.aai.aero/en/careers/recruitment"],
["Other PSU","CONCOR","https://www.concorindia.co.in/recruitment-notice?lang=hi"],
["Other PSU","BEML","https://www.bemlindia.in/careers/"],
["Other PSU","Bharat Dynamics","https://bdl-india.in/recruitments"],
["Other PSU","Cochin Shipyard","https://cochinshipyard.in/career"],
["Other PSU","GRSE","https://grse.in/job-openings/"],
["Other PSU","Goa Shipyard","https://goashipyard.in/notice-board/career/advertisement"],
["Other PSU","MIDHANI","https://midhani-india.in/department_hrd/career-at-midhani/"],
["Other PSU","MOIL","https://www.moil.nic.in/public/career"],
["Other PSU","Hindustan Copper","https://www.hindustancopper.com/Page/Career_new"],
["Other PSU","KIOCL","https://www.kioclltd.in/table.php?id=299&lang=EN"],
["Other PSU","GRID-INDIA","https://grid-india.in/en/careers/current-openings"],
["Other PSU","MRPL","https://www.mrpl.co.in/careers"],
["Other PSU","CPCL","https://www.cpcl.co.in/company/people/careers/"],
["Other PSU","Numaligarh Refinery","https://portal2.nrl.co.in/onlineapp/Home/CurrentOpenings"],
["Other PSU","WAPCOS","https://www.wapcos.co.in/english/career/"],
["Other PSU","NPCC","https://npcc.gov.in/Career.aspx"],
["Other PSU","SPMCIL","https://www.spmcil.com/en/discover-spmcil/"],
["Other PSU","IREDA","https://www.ireda.in/IredaWebPortal/careers/recruitmentnotifications"],
["Other PSU","IRFC","https://irfc.co.in/hi/recruitment-2026"],
["Other PSU","HUDCO","https://hudco.org.in/careers"],
["Other PSU","MSTC","https://www.mstcindia.co.in/MSTC_Careers/"],
["Other PSU","NHAI","https://nhai.gov.in/nhai/taxonomy/term/248"],
["Insurance","LIC","https://licindia.in/web/guest/careers"],
["Insurance","GIC Re","https://www.gicindia.com/careers/"],
["Insurance","National Insurance","https://nationalinsurance.nic.co.in/recruitment"],
["Insurance","New India Assurance","https://www.newindia.co.in/recruitment/list"],
["Insurance","Oriental Insurance","https://orientalinsurance.org.in/careers"],
["Insurance","United India Insurance","https://uiic.co.in/web/recruitment/details/201"],
["Insurance","Agriculture Insurance (AIC)","https://www.aicofindia.com/career"],
["Bank","SBI","https://sbi.bank.in/web/careers/current-openings"],
["Bank","Punjab National Bank","https://pnb.bank.in/Recruitments.aspx"],
["Bank","Bank of Baroda","https://bankofbaroda.bank.in/career/current-opportunities"],
["Bank","Canara Bank","https://www.canarabank.bank.in/pages/recruitment"],
["Bank","Union Bank of India","https://www.unionbankofindia.bank.in/en/common/recruitment"],
["Bank","Indian Bank","https://indianbank.bank.in/en/career"],
["Bank","Bank of India","https://bankofindia.bank.in/career/recruitment-notice"],
["Bank","Central Bank of India","https://centralbank.bank.in/en/recruitments"],
["Bank","Indian Overseas Bank","https://www.iob.bank.in/en/careers"],
["Bank","UCO Bank","https://uco.bank.in/job-opportunities"],
["Bank","Bank of Maharashtra","https://bankofmaharashtra.bank.in/current-openings"],
["Bank","Punjab & Sind Bank","https://punjabandsind.bank.in/content/recruitment"]];

KEY = re.compile(r"recruit|vacanc|advertisement|advt|notification|engagement|appointment of|apply|opening|apprentice|trainee|officer|executive|manager|\bposts?\b", re.I)
SKIP = re.compile(r"privacy|contact us|sitemap|home page|login|skip to|tender|\brti\b|annual report|terms", re.I)
DATE = re.compile(r"\b\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}\b|\b\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[,.]?\s+\d{4}\b", re.I)
ANCHOR = re.compile(r"<a\s[^>]*href\s*=\s*[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", re.I | re.S)
TAG = re.compile(r"<[^>]+>")
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
today = datetime.date.today().isoformat()

def parse(html, base):
    out, seen = [], set()
    for m in ANCHOR.finditer(html):
        text = re.sub(r"\s+", " ", TAG.sub(" ", m.group(2)).replace("&nbsp;", " ").replace("&amp;", "&")).strip()
        if not (12 <= len(text) <= 200) or text in seen or not KEY.search(text) or SKIP.search(text):
            continue
        href = m.group(1).strip()
        if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue
        seen.add(text)
        around = TAG.sub(" ", html[m.start(): m.end() + 250])
        d = DATE.search(around)
        out.append({"t": text, "u": urljoin(base, href), "d": d.group(0) if d else ""})
        if len(out) >= 6:
            break
    return out

def scan(i):
    cat, name, url = LINKS[i]
    items, err = [], ""
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        html = urlopen(req, timeout=25, context=ctx).read().decode("utf-8", "ignore")
        items = parse(html, url)
        if not items:
            err = "No postings readable here (site may load jobs with JavaScript). Open the official page."
    except Exception:
        err = "Could not reach the site right now. Open the official page."
    return i, items, err

prev = {}
if os.path.exists("data.json"):
    try:
        for r in json.load(open("data.json", encoding="utf-8"))["rows"]:
            prev[r["name"]] = r
    except Exception:
        pass

rows = [None] * len(LINKS)
with cf.ThreadPoolExecutor(8) as ex:
    for i, items, err in ex.map(scan, range(len(LINKS))):
        cat, name, url = LINKS[i]
        p = prev.get(name)
        old = {x["t"]: x.get("fs", "base") for x in (p["items"] if p else [])}
        for x in items:
            x["fs"] = old.get(x["t"]) or (today if p and p.get("checked") else "base")
        rows[i] = {"cat": cat, "name": name, "url": url, "items": items, "err": err, "checked": today}

now = datetime.datetime.utcnow().strftime("%d %b %Y, %H:%M UTC")
json.dump({"updated": now, "rows": rows}, open("data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Scanned", len(rows), "sites")
