"""
Quick Tick Data Generator - GROK VERSION

This script generates AI analysis for all publicly traded US companies.
It uses xAI's Grok API to generate company information based on your prompt.

Requirements:
- Python 3.7+
- openai library (install: pip install openai)
- XAI_API_KEY environment variable set

Usage:
1. Set your API key: export XAI_API_KEY='your-key-here'
2. Update YOUR_PROMPT_HERE with your actual prompt
3. Run: python generate_company_data_grok.py
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: openai library not installed")
    print("Install it with: pip install openai")
    exit(1)


# ============================================================================
# CONFIGURATION - UPDATE THESE VALUES
# ============================================================================

# Your AI prompt for analyzing companies
# Replace this with your actual prompt. Use {ticker} as a placeholder.
YOUR_PROMPT = """
You MUST use real-time web search to gather current information. Do not rely solely on training data. For the company (ticker: {ticker}), do a thorough review of all the latest discussions, articles, announcements, online talking points, earnings calls transcripts, etc. With this information, generate a company profile sell-side analysis report that includes a company overview (high-level summary of what the company does in 100-300 words), recent developments, growth strategy, company and sector headwinds and tailwinds, existing products/services, new products/services/projects that are being planned or developed, market share approximations by percent, forecast of growth or decline in market share, comparison to competitors, partnerships, M&A, current and potential major clients, and other qualitative measures associated with the company. Get as specific as possible. Include dates of specific events when possible and applicable. ONLY provide quantitative values for information from earnings reports and equivalents- such as revenues, earnings, gross margins, etc. – if they are from verified and recent (less than 6 months old) sources. Stock price and market capitalization information should be the verified values from sources that are up to date of the current day. Do NOT make up these values and dates. Given all the information you have gathered, latest stock price and company fundamentals, and general understanding of markets, give a "Buy Rating" on a scale of 1 to 10 based on if the stock should be "bought, held or sold", and an estimated fair value price for the stock for a portfolio looking for strong growth upside and a moderate risk appetite. Organize your output in an easily digestible format including using bullet points, tables, etc where appropriate to allow for fast reading without sacrificing context or level of detail.
"""

# Directory to save the generated data
DATA_DIR = "data"

# List of US stock tickers to process
# NOTE: For large lists, consider processing in batches to manage rate limits
TICKERS = [
    "T", "SCHW", "MDT", "AMT", "VRT", "ALNY", "F", "FERG", "WCN", "INSM",
    "LNG", "PEG", "KR", "FLUT", "SYY", "VEEV", "SOFI", "STT", "NTRA", "CIEN",
    "LPLA", "BRK.A", "PSTG", "RDDT", "CRDO", "MKL", "HEI.A", "K", "UTHR", "CW",
    "CASY", "ZM", "FWONK", "RKLB", "EXAS", "ILMN", "THC", "FTI", "HUBS", "SGI",
    "RBA", "RKT", "GWRE", "WWD", "AFRM", "TLN", "TWLO", "SSNC", "FTAI", "USFD",
    "NVT", "FCNCA", "TRU", "FN", "BWXT", "SUI", "BURL", "XPO", "DKNG", "JLL",
    "FNF", "RIVN", "PFGC", "NBIX", "CRS", "PINS", "APG", "WPC", "EWBC", "RS",
    "NLY", "ITT", "RBC", "EQH", "DOCU", "ATI", "CG", "RPM", "TOL", "ACM",
    "GGG", "CACI", "CSL", "OKTA", "OHI", "U", "MTZ", "RGLD", "DT", "MEDP",
    "LECO", "DKS", "RVMD", "WCC", "NXT", "KTOS", "Z", "GH", "BLD", "TW",
    "ROKU", "IONS", "RGA", "BBIO", "DTM", "UNM", "RNR", "NTNX", "WSO", "QXO",
    "WMS", "SF", "BJ", "EVR", "ENTG", "EHC", "GLPI", "TXRH", "ELAN", "MLI",
    "LAMR", "ASTS", "FHN", "SNX", "EXEL", "ALLY", "CCK", "AYI", "W", "MTSI",
    "WTRG", "ELS", "CLH", "AGNC", "PEN", "AA", "BMRN", "HL", "ENSG", "AR",
    "MDGL", "OKLO", "MANH", "SCI", "CDE", "MKSI", "OVV", "AVAV", "DCI", "CMA",
    "RMBS", "IOT", "BAH", "PR", "GMED", "ORI", "JAZZ", "SPXC", "AMH", "STRL",
    "DY", "NYT", "REXR", "WBS", "RNA", "AFG", "AIT", "ARMK", "SATS", "RRX",
    "EGP", "HLI", "OC", "FYBR", "PLNT", "OWL", "FLS", "BWA", "AAL", "IDCC",
    "OGE", "GTLS", "CNM", "RGEN", "TTEK", "HQY", "FIVE", "GME", "SSB", "CR",
    "RRC", "SEIC", "WTFC", "AHR", "WAL", "KNSL", "MOD", "CUBE", "ROIV", "UGI",
    "DINO", "HALO", "PRI", "CRBG", "JEF", "PCOR", "COLB", "ADC", "SNAP", "CTRE",
    "CART", "SFM", "OSK", "ATR", "AWI", "LAD", "COKE", "RBRK", "VMI", "CYTK",
    "BRX", "AVTR", "AEIS", "LYFT", "QRVO", "SANM", "ZION", "LNC", "NNN", "ONB",
    "G", "JOBY", "CNH", "LKQ", "ZWS", "UMBF", "AXS", "FR", "WTS", "SOLS",
    "OLLI", "CFR", "SAIA", "LUMN", "TPG", "NFG", "CLF", "ALSN", "WING", "MASI",
    "HIMS", "STAG", "OMF", "JBTM", "BPOP", "CADE", "EXP", "RYTM", "AMG", "DUOL",
    "HEI", "CMC", "AN", "EMN", "IDA", "CORT", "PNFP", "KNX", "BROS", "ONTO",
    "SSD", "ARWR", "FLR", "INGR", "CHDN", "TTC", "CHWY", "FND", "PTCT", "VFC",
    "JXN", "CBSH", "TTMI", "MAT", "VOYA", "AGCO", "R", "MUSA", "FSS", "GAP",
    "H", "MTG", "ORA", "AXTA", "PCTY", "MOG.A", "PRIM", "EAT", "TRNO", "ESAB",
    "PCVX", "AAON", "AXSM", "HR", "SMTC", "CHE", "STWD", "AL", "FAF", "VNO",
    "CWAN", "SNV", "LFUS", "KEX", "SEE", "DOCS", "RYAN", "EPRT", "IBP", "SITM",
    "PB", "FBIN", "VNOM", "CRUS", "TXNM", "BSY", "MHK", "EXLS", "NEU", "RITM",
    "HXL", "MIR", "AM", "IRTC", "CWST", "BIO", "CIFR", "SITE", "FCFS", "MSA",
    "THG", "ESI", "KD", "FNB", "AUR", "BOOT", "TMHC", "ESNT", "BFAM", "LIF",
    "GTES", "SLM", "MKTX", "COGT", "GXO", "KMX", "GKOS", "M", "NOV", "RDNT",
    "LEA", "RHP", "LAZ", "ULS", "FROG", "GATX", "KRYS", "ACI", "PIPR", "HRB",
    "PTGX", "WH", "POR", "RAL", "ARW", "NXST", "ESE", "NUVL", "DAR", "LBRDK",
    "CVLT", "COMP", "UEC", "JHG", "DBX", "MORN", "MIDD", "GTLB", "RLI", "CHRD",
    "VLY", "WFRD", "ENS", "OLED", "BKH", "SWX", "THO", "CDTX", "VNT", "KBR",
    "FCN", "UBSI", "BMI", "ACA", "GBCI", "CNX", "MTN", "GPI", "LMND", "BRKR",
    "ROAD", "UFPI", "LPX", "MMSI", "AGX", "TKR", "ETSY", "KRG", "QLYS", "WEX",
    "KRC", "OPCH", "BCPC", "TFX", "OGS", "GNTX", "HOMB", "WTM", "MTH", "SR",
    "OZK", "ALK", "ABCB", "ALKS", "HWC", "HLNE", "MMS", "ACIW", "CAVA", "AUB",
    "NJR", "OPEN", "RDN", "POST", "GPK", "SIGI", "TGTX", "MC", "MTDR", "QS",
    "TMDX", "APPF", "PRAX", "MRP", "NPO", "FOUR", "CVCO", "GVA", "ECG", "BILL",
    "BYD", "SBRA", "ST", "CORZ", "URBN", "SKY", "CZR", "WK", "UHAL.B", "CE",
    "CSW", "ABG", "WULF", "CCC", "PSN", "LSTR", "ITRI", "TTAN", "PI", "AMKR",
    "BDC", "ADT", "HRI", "PECO", "ANF", "BCO", "LOPE", "REZI", "RUN", "AX",
    "MAC", "CROX", "VSAT", "MDU", "ADMA", "MUR", "BC", "SPR", "OSIS", "CUZ",
    "WHR", "LEU", "QTWO", "CRNX", "ACHR", "HASI", "STEP", "HUT", "NWE", "RIG",
    "FORM", "KNF", "TNL", "LEN.B", "WAY", "AMTM", "SON", "ATMU", "SXT", "MARA",
    "AKRO", "COMM", "ASB", "KTB", "BTSG", "HCC", "TCBI", "DLB", "ELF", "AROC",
    "NOVT", "AGO", "MGY", "FLG", "PVH", "BOX", "SAIC", "EBC", "CLSK", "ACLX",
    "SNEX", "IRT", "LNTH", "VIAV", "MSGS", "SLAB", "EPR", "VVV", "AVT", "MSM",
    "FTDR", "VSEC", "VKTX", "SIG", "SIRI", "ALE", "HAE", "WMG", "CNR", "PRM",
    "CELC", "LAUR", "SKYW", "BRBR", "NE", "LLYVK", "PJT", "KYMR", "PLXS", "CWK",
    "PFSI", "FFIN", "PRMB", "OSCR", "MWA", "MRCY", "CNO", "LGND", "FHI", "TREX",
    "BHF", "IESC", "ZG", "VCYT", "KBH", "TDS", "IBOC", "UCB", "LTH", "BBWI",
    "INSP", "EXPO", "DORM", "SKT", "SRRK", "INDB", "FELE", "NHI", "ENPH", "PII",
    "GNW", "VRNS", "GPOR", "SFBS", "ICUI", "SHC", "NVST", "CDP", "MHO", "PATK",
    "OTTR", "RYN", "KFY", "APGE", "CALM", "WSC", "HAYW", "CRC", "SLGN", "GRAL",
    "GHC", "SLG", "RNST", "YETI", "VCTR", "AVA", "KVYO", "SHAK", "OUT", "CBT",
    "ARQT", "MYRG", "VRRM", "FULT", "MATX", "KAI", "ZETA", "CPK", "BKU", "BRC",
    "CALX", "VAL", "PSMT", "ASO", "ALGM", "MZTI", "YOU", "TENB", "AEO", "BGC",
    "PLMR", "ATGE", "BL", "CATY", "RARE", "BNL", "BXMT", "FBP", "ACAD", "UUUU",
    "SPSC", "TVTX", "GFF", "FUL", "BTU", "ENVA", "WGS", "VSCO", "TGNA", "POWL",
    "MIRM", "WSFS", "AAP", "AGYS", "COLD", "CGON", "FHB", "AIR", "GSAT", "TPC",
    "HGV", "FOLD", "SHOO", "SARO", "DOCN", "TARS", "MGEE", "HIW", "CBU", "AZZ",
    "BFH", "HOG", "RRR", "PCH", "IDYA", "SXI", "NMIH", "WSBC", "DAN", "WHD",
    "PBH", "LOAR", "EEFT", "VIRT", "TEX", "CPRI", "RUSHA", "BCC", "CNK", "HURN",
    "CARG", "ADPT", "AWR", "WU", "TPH", "VC", "VRDN", "AVNT", "TBBK", "FRPT",
    "DYN", "PBF", "APAM", "SBCF", "FIBK", "BLKB", "LBRT", "FRSH", "CWEN", "CXT",
    "LXP", "NSIT", "DRS", "NATL", "CPRX", "CIVI", "KGS", "KAR", "PRVA", "CWT",
    "PL", "AKR", "ABM", "SFNC", "HHH", "WDFC", "ALHC", "PTON", "PAG", "LRN",
    "RHI", "BOH", "INSW", "LCII", "KSS", "MPW", "ACLS", "MCY", "NCNO", "UNF",
    "TDC", "CVBF", "ONDS", "MGRC", "BKD", "ITGR", "APLE", "GTM", "CRWV", "ATEC",
    "CBZ", "DAVE", "FCPT", "SYNA", "HP", "CON", "BOKF", "WAFD", "REVG", "UPWK",
    "INTA", "LINE", "JOE", "DNOW", "ALRM", "HWKN", "XMTR", "OII", "NMRK", "SMG",
    "SUPN", "OLN", "IRON", "MTRN", "KMPR", "UE", "FBK", "ASH", "SLNO", "PLUS",
    "PFS", "RH", "DXC", "GT", "IAC", "EWTX", "PLUG", "DNLI", "BANC", "CHH",
    "TOWN", "BEAM", "COCO", "RNG", "APLS", "TDW", "XRAY", "CURB", "FFBC", "HI",
    "ATKR", "PRK", "CHEF", "HUBG", "RELY", "NUVB", "SPHR", "KRMN", "EXTR", "DK",
    "PARR", "ADUS", "GOLF", "TERN", "IVT", "FWONA", "AMRX", "SM", "CSGS", "RXO",
    "EYE", "PENN", "TRN", "CAR", "STC", "UNFI", "PTEN", "BBT", "WLK", "MLYS",
    "CAKE", "SONO", "BRZE", "GEO", "AORT", "MGNI", "TRMK", "KMT", "LQDA", "MD",
    "WD", "CUBI", "CACC", "OI", "GRBK", "NOG", "LEVI", "VICR", "CRVL", "AVPT",
    "RCUS", "SPNT", "BANR", "TXG", "FLO", "PGNY", "NBTB", "EPAC", "HE", "DIOD",
    "BANF", "OCUL", "SYRE", "SEI", "NSA", "VCEL", "FRME", "NWN", "FBNC", "PHIN",
    "OLMA", "OGN", "SMMT", "SRPT", "BUSE", "AVDL", "NNI", "WRBY", "HCI", "LC",
    "ARR", "CRK", "DEI", "BWIN", "DDS", "CNXC", "CC", "NGVT", "KWR", "EFSC",
    "MSGE", "CTRI", "RXRX", "SYBT", "MQ", "POWI", "ASGN", "HMN", "QDEL", "DRH",
    "EVTC", "IOSP", "DX", "IPGP", "CLDX", "NTCT", "MTX", "PK", "PRGO", "TWST",
    "CXW", "LION", "SDRL", "PPC", "HLIO", "HNI", "RAMP", "FMC", "SMPL", "PRGS",
    "SKWD", "CNS", "SHO", "BELFB", "OFG", "GEF", "DJT", "DBRG", "GNL", "NWBI",
    "KN", "VECO", "VERA", "NTST", "CCS", "HUN", "IE", "HRMY", "BKE", "YELP",
    "ENOV", "GSHD", "HLMN", "TNET", "CASH", "SNDX", "VAC", "ATRC", "ATRO", "NHC",
    "LMAT", "AGIO", "SCS", "VSH", "CHCO", "IMVT", "CRGY", "STRA", "LTC", "ACMR",
    "PAYO", "LCID", "PRCT", "AMR", "ANDE", "RSI", "UFPT", "KNSA", "ALG", "BLBD",
    "WOR", "OS", "SEM", "PRDO", "SLVM", "TPB", "GTY", "LZ", "LZB", "STOK",
    "FLYW", "FCF", "AAOI", "OMCL", "LASR", "CLMT", "SBH", "CENTA", "STBA", "ANIP",
    "CECO", "BATRK", "NEO", "MNKD", "CENX", "TRIP", "ELME", "DBD", "SAM", "FSLY",
    "AGM", "TILE", "ROG", "NWL", "MODG", "BHE", "PBI", "HTH", "ACHC", "BCRX",
    "LLYVA", "KNTK", "NIC", "IRDM", "KALU", "ABR", "CWEN.A", "HTO", "ROCK", "DGII",
    "DV", "IMNM", "WT", "JJSF", "WERN", "ARLO", "XPRO", "ICFI", "DNTH", "PCT",
    "LKFN", "STEL", "FIVN", "AMLX", "IPAR", "ARI", "CCB", "PAY", "TALO", "COLL",
    "TNDM", "NBHC", "AIN", "AZTA", "WLDN", "ZYME", "MBC", "PAR", "UPB", "SHLS",
    "ARCB", "WLY", "IIPR", "FDP", "VERX", "FUN", "NSSC", "HCSG", "SPB", "VVX",
    "NVCR", "TRVI", "TIC", "NVRI", "DVAX", "NRIX", "MAN", "TNC", "HOUS", "CNMD",
    "PEB", "ZD", "TDOC", "COLM", "GABC", "XHR", "EFC", "REAL", "SGRY", "ALKT",
    "JANX", "JBLU", "ARDX", "VYX", "GBX", "LEG", "SILA", "PLAB", "HROW", "PZZA",
    "WINA", "QCRH", "REYN", "INVA", "RLAY", "NEOG", "DCO", "PACS", "TCBK", "HOPE",
    "WEN", "FLNC", "ADEA", "ACVA", "AMC", "LADR", "DFIN", "TRS", "NKTR", "LNN",
    "FIGR", "UVV", "AXGN", "WWW", "CTS", "HLF", "ENR", "PRLB", "PRA", "MCRI",
    "PGRE", "MBX", "TFIN", "XNCR", "BBNX", "DCOM", "AAMI", "WKC", "MXL", "USLM",
    "CNOB", "CDRE", "WABC", "ALGT", "BF.A", "ATEN", "NSP", "PFBC", "CMPR", "BFC",
    "DXPE", "SVRA", "TNGX", "BLFS", "HSII", "COTY", "PHR", "UMH", "JBGS", "FTRE",
    "ARRY", "THR", "WS", "LGN", "ECPG", "ACT", "TRUP", "ALEX", "UTI", "CSR",
    "EYPT", "NEXT", "USPH", "SEB", "UWMC", "IMKTA", "VITL", "CERT", "PMT", "CRI",
    "SION", "CRAI", "ASAN", "PDM", "LOB", "PRG", "UCTT", "FA", "NVAX", "OBK",
    "RLJ", "AMRC", "VRE", "SAFT", "FWRG", "SDGR", "COHU", "GIII", "EZPW", "MLKN",
    "PWP", "KURA", "TWO", "XERS", "FUBO", "PD", "SEZL", "DHC", "CSTL", "CVI",
    "HLIT", "OCFC", "ASTH", "VRTS", "TSHA", "GO", "NN", "JAMF", "XPEL", "SAIL",
    "LGIH", "THS", "IAS", "PCRX", "PENG", "KW", "GRC", "ORKA", "WTTR", "ASTE",
    "INVX", "MFA", "ORC", "PEBO", "EXPI", "IDT", "MAZE", "PRO", "ECVT", "ORIC",
    "OSBC", "THRM", "ALIT", "PRKS", "CIM", "AHCO", "AMPH", "EIG", "INBX", "SCL",
    "RVLV", "NTLA", "RPD", "WGO", "SRCE", "ELVN", "LUNR", "ALH", "ESRT", "NPKI",
    "PHAT", "PRCH", "PVLA", "GBTG", "CLOV", "SNDR", "DEA", "TTI", "ESPR", "MSEX",
    "HLX", "STAA", "SAH", "REX", "VTOL", "CDNA", "UNIT", "AAT", "DLX", "COUR",
    "UVSP", "WMK", "AVBP", "CCOI", "CTBI", "BV", "CXM", "UTL", "ZBIO", "ROOT",
    "UPBD", "RAPP", "SMA", "BETA", "NTSK", "ARVN", "PDFS", "IART", "BBSI", "GLUE",
    "SEPN", "MEG", "PNTG", "RIGL", "FBRT", "YEXT", "IAUX", "TMP", "UVE", "PAHC",
    "RAPT", "DRVN", "AMPL", "SBSI", "ANAB", "FMBH", "BHRB", "HAFC", "HFWA", "EPC",
    "FIGS", "SMP", "GLDD", "HBNC", "JBI", "SCSC", "IOVA", "ODP", "BJRI", "VSTM",
    "NAVI", "TFSL", "PUMP", "ALNT", "FIZZ", "SIBN", "DAKT", "AD", "CMP", "KOD",
    "AMWD", "CNNE", "AIV", "PRSU", "GLIBK", "PLYM", "BCAX", "TRST", "IRMD", "LENZ",
    "BY", "TBPH", "LFST", "NBBK", "QNST", "ERII", "CPF", "MDXG", "LBRDA", "RHLD",
    "HPP", "MCB", "SLDP", "RZLT", "SAFE", "AMTB", "EMBC", "CFFN", "SNCY", "ESQ",
    "EVER", "ERAS", "LMB", "METC", "AMSF", "TDUP", "DAWN", "NTGR", "CCNE", "RWT",
    "BRSP", "MBWM", "VSTS", "MIAX", "GOSS", "GERN", "MATW", "MMI", "VIR", "EQBK",
    "AXL", "JBSS", "PLOW", "BLND", "APOG", "TDAY", "SANA", "BFST", "UA", "CMPX",
    "NIQ", "FWRD", "VG", "NBR", "RCAT", "CARS", "AVAH", "CNXN", "IBRX", "SEMR",
    "UAA", "BZH", "ABUS", "HRTG", "BBW", "IBCP", "MBIN", "MYGN", "ADAM", "MYE",
    "UTZ", "KE", "RUSHB", "HNGE", "CTLP", "PACB", "ORRF", "GDOT", "TYRA", "CRMD",
    "CAC", "TR", "KALV", "WSR", "FG", "UFCS", "AQST", "MATV", "CWH", "CBRL",
    "CBL", "HTZ", "CTMX", "VTYX", "GPRE", "AESI", "AMN", "CGEM", "HTBK", "AEHR",
    "DJCO", "MOFG", "NRDS", "FULC", "ADTN", "EE", "RYI", "UAMY", "OMER", "OPY",
    "GES", "RBCAA", "HYMC", "ANNX", "TREE", "THFF", "NX", "MPB", "SG", "NXRT",
    "CTKB", "HNRG", "ACEL", "CMPO", "TRTX", "VTS", "RGNX", "HTB", "SABR", "MTUS",
    "PRAA", "RUM", "HSTM", "INDI", "BW", "OFIX", "GHM", "PX", "PSNL", "BOW",
    "FLGT", "SENEA", "ALMS", "GSBC", "NAVN", "HOV", "NBN", "PGEN", "CRVS", "CTEV",
    "FISI", "CCO", "MRTN", "SBGI", "AIOT", "EBS", "BDN", "IVVD", "CSV", "SMBC",
    "ETD", "STGW", "INN", "CASS", "ATXS", "CTO", "KOP", "NABL", "DFH", "SHEN",
    "IIIN", "HIPO", "WASH", "CCBG", "LQDT", "SXC", "FOXF", "VTLE", "GDEN", "GDYN",
    "LINC", "ODC", "OXM", "LXEO", "ICHR", "TCMD", "NWPX", "FCBC", "IIIV", "IVR",
    "SMBK", "ASPI", "YORW", "REPL", "CWCO", "NRIM", "CEVA", "MBUU", "UHT", "KFRC",
    "HGTY", "SHBI", "EGBN", "APEI", "FDMT", "KODK", "RES", "GRDN", "SPRY", "MNRO",
    "CABO", "AVNS", "UHAL", "BLMN", "GOGO", "FFIC", "BFLY", "ARHS", "CPS", "HTFL",
    "OPK", "BLLN", "AHH", "FSBC", "MCW", "IDR", "LYTS", "PLPC", "SSTK", "NPK",
    "CLB", "TRNS", "GOOD", "GOLD", "OPTU", "BXC", "MH", "BWMN", "AVO", "MCBS",
    "MAGN", "SPT", "SCHL", "CODI", "UDMY", "TROX", "APPS", "GEVO", "GCMG", "PKST",
    "AMAL", "FMNB", "AOSL", "IRWD", "SKYT", "TE", "ANGO", "FSUN", "AROW", "HIFS",
    "VREX", "ALX", "BCAL", "FOR", "RGR", "CBLL", "SERV", "BKV", "SPFI", "EVH",
    "ARX", "ALT", "NUS", "NLOP", "NAGE", "CYRX", "DIN", "GTN", "PLAY", "KREF",
    "URG", "MRVI", "COFS", "JBIO", "BHB", "ZVRA", "LXU", "LIND", "CMCO", "AXTI",
    "ALRS", "ACNB", "PSIX", "FIP", "NP", "HZO", "OSPN", "IMXI", "SD", "MLR",
    "NPB", "XOMA", "SFIX", "CYH", "TCBX", "CLBK", "SLDE", "HELE", "NPCE", "BSRR",
    "EHAB", "ANGI", "EBF", "IHRT", "NFBK", "AIP", "PFIS", "LAB", "PGC", "ABSI",
    "TIPT", "IBTA", "GMRE", "RXST", "CLMB", "DC", "CARE", "MLAB", "CHCT", "CIVB",
    "WRLD", "RYAM", "EVGO", "LYEL", "GRPN", "TALK", "AKBA", "VPG", "OSG", "VIA",
    "SWIM", "MNPR", "FRBA", "CMTG", "FBIZ", "CCSI", "FFWM", "SFST", "DNA", "RC",
    "WEAV", "REPX", "SES", "EOLS", "ZEUS", "CLPT", "ASIX", "FRGE", "CAL", "ULCC",
    "GCO", "NUTX", "ZUMZ", "OCGN", "GRND", "BMRC", "FPI", "IMRX", "TWI", "CWBC",
    "GIC", "MAMA", "ASMB", "BFS", "FLY", "BAND", "MITK", "MTW", "TITN", "EVEX",
    "ORN", "NXDR", "KOPN", "KRNY", "OIS", "KMTS", "ENTA", "EGY", "HBCP", "ITIC",
    "JACK", "PKE", "ETON", "NGVC", "PUBM", "SWBI", "BETR", "CTOS", "PRME", "SITC",
    "DOMO", "WTBA", "MAX", "MCS", "FET", "NGS", "CLNE", "TWFG", "HTLD", "BGS",
    "BWB", "SVV", "OLP", "DGICA", "GRNT", "UNTY", "TRC", "BIOA", "CLFD", "CVGW",
    "WNC", "MBI", "MGPI", "PSTL", "PTLO", "LXFR", "ANRO", "BCML", "PTRN", "DNUT",
    "MSBI", "GLRE", "AVBC", "KROS", "BOC", "BBBY", "ORGO", "GBFH", "ABAT", "ABL",
    "SOC", "ILPT", "CCRN", "SLDB", "LCTX", "DHIL", "CERS", "HVT", "LAND", "RBB",
    "FSBW", "CLDT", "XRX", "PDLB", "CBNK", "MOV", "RDW", "AVXL", "FLOC", "TBRG",
    "ATLC", "TRDA", "ALDX", "NRC", "BYRN", "BNC", "BATRA", "CRSR", "STRT", "AURA",
    "MVBF", "EAF", "NVEC", "MTRX", "ACCO", "ZIP", "DCTH", "CVLG", "VENU", "DENN",
    "VLGEA", "VNDA", "KRUS", "LPTH", "KIDS", "MCFT", "NCMI", "SMC", "IPI", "FVR",
    "CBAN", "CDZI", "MEC", "TLS", "RCKT", "RM", "CMRC", "SCVL", "CNDT", "SLP",
    "SMRT", "QTRX", "SSP", "HBT", "PEPG", "CZNC", "BWFG", "FMAO", "PCB", "SNWV",
    "DSGN", "ACRS", "VOYG", "HY", "MVIS", "CLW", "SVC", "HLLY", "NEWT", "RRBI",
    "SGHT", "MG", "MCHB", "OOMA", "BRBS", "NATR", "AVTX", "ARTNA", "DSGR", "ACRE",
    "SMLR", "GNE", "TARA", "AMCX", "USCB", "CIA", "LOCO", "ONIT", "OBT", "FRPH",
    "DDD", "OPFI", "ARKO", "WNEB", "RNGR", "ASPN", "BMBL", "WSBF", "SRTA", "PLSE",
    "ATEX", "TOI", "TSBK", "WOW", "CIO", "KELYA", "FRST", "LXRX", "BNTC", "MBCN",
    "HDSN", "MEI", "ISTR", "BLFY", "RPAY", "XPER", "LMNR", "TH", "RMNI", "BVS",
    "PINE", "FBLA", "AVNW", "CZFS", "WLFC", "RBBN", "AII", "NECB", "CTRN", "ABEO",
    "GALT", "CBIO", "GDRX", "PKBK", "EGHT", "CRD.B", "RR", "HYLN", "JMSB", "HNST",
    "OPRX", "BALY", "TECX", "SNDA", "III", "FUNC", "WOOF", "ACHV", "LDI", "FNLC",
    "PYXS", "AVIR", "ALTS", "PLBC", "MPAA", "SIGA", "KYTX", "THRY", "FCCO", "ACIC",
    "FSTR", "NGNE", "FENC", "CTNM", "FRAF", "SPOK", "ALLO", "UMAC", "PACK", "RMR",
    "EGAN", "EFSI", "FBRX", "CABA", "XFOR", "MITT", "WEST", "USNA", "NFE", "RLGT",
    "LRMR", "QSI", "RCKY", "VABK", "VYGR", "JCAP", "CAPR", "MFIN", "PBYI", "CRCT",
    "PCYO", "EDIT", "NWFL", "PESI", "CFFI", "CHMG", "CVRX", "JELD", "SPCE", "AMPY",
    "TBCH", "REKR", "ELMD", "BRY", "NATH", "OVLY", "PKOH", "IMMR", "LFCR", "ATLO",
    "BPRN", "KRMD", "TG", "DOUG", "FVCB", "REFI", "FEIM", "JRVR", "ATNI", "BH",
    "INR", "MYFW", "OMI", "BLZE", "VMD", "TASK", "AGL", "NMRA", "CTGO", "SENS",
    "KRT", "ARDT", "ASUR", "SLQT", "CENT", "ASLE", "KFS", "CRBP", "HCAT", "LOVE",
    "ONTF", "CURI", "WEYS", "RICK", "HWBK", "GPRO", "SLS", "BKTI", "OWLT", "TWIN",
    "TSSI", "SPIR", "LCNB", "AREC", "GETY", "LPRO", "STRS", "FDBC", "BKKT", "BSVN",
    "TRAK", "SKYH", "EB", "LNKB", "INV", "QUAD", "PPIH", "CZWI", "MRBK", "CCCC",
    "UTMD", "FXNC", "NC", "TCX", "JOUT", "OPRT", "ALTO", "VTGN", "INFU", "CADL",
    "RGCO", "GYRE", "SDHC", "SGMT", "OPBK", "PAL", "HUMA", "LE", "MNTN", "VEL",
    "VUZI", "NKSH", "FFAI", "PEBK", "GEOS", "FC", "XPOF", "FLXS", "SMHI", "BVFL",
    "USAU", "UIS", "BHR", "KINS", "LAW", "FRMI", "PBFS", "TRUE", "BNED", "ASIC",
    "DBI", "HRTX", "CRBU", "ISBA", "GNLX", "AOMR", "INGN", "OMDA", "LEGH", "HPK",
    "IKT", "ECBK", "CHPT", "WTI", "DIBS", "PAYS", "DUOT", "OSUR", "ACR", "GEMI",
    "POWW", "EVC", "REI", "TNYA", "CBFV", "OBIO", "SEG", "SUIG", "ACTG", "FINW",
    "DSP", "MASS", "BDTX", "RMBI", "CRMT", "CHRS", "ARCT", "TTSH", "FTK", "FHTX",
    "RMAX", "BBCP", "FSFG", "PRTH", "MXCT", "SBFG", "FCEL", "ALCO", "FLD", "FOA",
    "BSET", "BRT", "GIFI", "LWAY", "RGP", "TAYD", "CRDF", "QNCX", "DVLT", "LTRX",
    "MRAM", "CMT", "GCBC", "OABI", "TTGT", "GSIT", "INBK", "SRI", "TNXP", "AGEN",
    "LODE", "CDXS", "STXS", "SKYX", "OVBC", "STRZ", "SMID", "MNSB", "ALTI", "SATL",
    "SAVA", "DMRC", "SAMG", "HNVR", "CATX", "TLSI", "GENC", "BFIN", "TGEN", "GPMT",
    "FOSL", "HOFT", "TBI", "INO", "STEM", "ONEW", "FNWD", "TMCI", "BTCS", "ANIK",
    "SRBK", "UBFO", "EBMT", "JAKK", "KLC", "FRD", "ANIX", "SNFCA", "SEVN", "LAKE",
    "QIPT", "SGC", "INSG", "WHG", "LARK", "DH", "AARD", "HBB", "XGN", "ISSC",
    "ONL", "ESCA", "SRG", "LFMD", "STEX", "VOR", "APYX", "EVI", "ARQ", "MBOT",
    "ALTG", "KLTR", "FONR", "BLNK", "JYNT", "MDV", "ELDN", "NAUT", "GWRS", "AREN",
    "ACNT", "AMBQ", "MRSN", "RELL", "INTT", "AVD", "MCRB", "SKIN", "ACU", "KVHI",
    "ELA", "ASYS", "FBYD", "SPWR", "KRO", "BOOM", "OVID", "RPT", "SRZN", "EWCZ",
    "KULR", "DFDV", "COYA", "BCBP", "MED", "PDEX", "FNKO", "OLPX", "SCLX", "EPM",
    "GLIBA", "JILL", "NREF", "FATE", "ULH", "NXDT", "ALEC", "ARAY", "MPTI", "MLP",
    "AOUT", "EHTH", "SUNS", "SNBR", "CGTX", "AMTX", "IRD", "CFBK", "INNV", "RVSB",
    "KEQU", "NPWR", "HURA", "CARL", "CNTX", "CLAR", "CHGG", "CSPI", "ZVIA", "HAIN",
    "RAIL", "EML", "STHO", "MNTK", "HURC", "CCLD", "RCMT", "HFFG", "UNCY", "VIRC",
    "LUCK", "AEYE", "EPSN", "ATOS", "RCEL", "ESOA", "SPRO", "SEER", "PLBY", "PEW",
    "MGNX", "QMCO", "GNSS", "AIRO", "GORO", "LGCY", "BARK", "PLRX", "LNSR", "FSP",
    "CBNA", "LUCD", "TYGO", "DCGO", "NVCT", "KG", "EXOD", "STRW", "FLL", "SRFM",
    "ELTX", "TTEC", "MPX", "INVE", "STTK", "SGMO", "PROV", "NKTX", "RPID", "FF",
    "MAPS", "GUTS", "GRWG", "CXDO", "EXFY", "CMTL", "QUIK", "CPSS", "ANVS", "NODK",
    "RSSS", "FORR", "OM", "VHC", "AXR", "HYPR", "RILY", "CRVO", "PMTS", "UNB",
    "SERA", "SND", "OFLX", "BMNR", "SPWH", "DERM", "AISP", "FNWB", "STIM", "DHX",
    "CHMI", "ADVM", "FDSB", "BRCC", "ALMU", "WRAP", "NRDY", "WWR", "SWKH", "CTM",
    "CHYM", "BTMD", "RXT", "BH.A", "BYND", "CLST", "ATOM", "NTIC", "ZNTL", "ACTU",
    "CHCI", "STRO", "AVBH", "RDNW", "IMMX", "METCB", "VRA", "LFVN", "RNAC", "SPRU",
    "ABOS", "ASRT", "WHWK", "APT", "SRTS", "ATYR", "FTLF", "BMEA", "AIRJ", "IZEA",
    "ESP", "PZG", "SMTI", "RRGB", "BWEN", "GLIBR", "FBIO", "ASPS", "PMVP", "ATRA",
    "QVCGA", "ULBI", "SSBI", "BOTJ", "DLHC", "CODA", "CYPH", "FTCI", "CATO", "LUNG",
    "CDLX", "ALOT", "HNNA", "FSI", "HGBL", "IMUX", "SSTI", "TSQ", "WYY", "NNBR",
    "OPAL", "CVGI", "TZOO", "LAZR", "CPBI", "MYPS", "PLCE", "AIRS", "UPLD", "FSEA",
    "OTLK", "TCRX", "GAIA", "UP", "UFI", "NSTS", "BGSF", "OPTT", "PROP", "CLYM",
    "STKS", "SELF", "WBI", "COSO", "NXXT", "VTSI", "BYFC", "DTIL", "CNTY", "BAER",
    "SACH", "PRLD", "LFT", "COOK", "AFBI", "ONMD", "DXLG", "WYFI", "ORGN", "SGA",
    "DLTH", "AMWL", "LCUT", "OKUR", "TKNO", "RJET", "JSPR", "SKIL", "TIL", "PAMT",
    "RFIL", "CSBR", "FLWS", "RBKB", "WFCF", "AFCG", "STUB", "GCTS", "HQI", "PTHS",
    "CIX", "AIRG", "CLPR", "ASRV", "IRBT", "CPSH", "KZR", "UAVS", "PXLW", "AWRE",
    "ARMP", "SLSN", "PHUN", "CAI", "TENX", "EVMN", "CULP", "KRRO", "RANI", "TELA",
    "NTWK", "FKWL", "FTEK", "ALXO", "GLSI", "ACET", "SNCR", "MGX", "NL", "CBC",
    "PNRG", "PRPL", "GRCE", "GAME", "ATNM", "EQ", "KPTI", "TISI", "PBHC", "SI",
    "OESX", "UEIC", "LOAN", "MIND", "LVO", "TACT", "BSBK", "VRCA", "OCC", "RNTX",
    "OPXS", "ALGS", "CVM", "CALC", "IMDX", "BRCB", "VANI", "AP", "KLRS", "PBBK",
    "INUV", "TELO", "SEAT", "BCAB", "BEEP", "STRR", "OPAD", "TVRD", "DOMH", "PSQH",
    "USIO", "PETS", "CBUS", "MCHX", "EP", "FORA", "NDLS", "AUBN", "IMA", "SIEB",
    "CTSO", "CURV", "ZDGE", "SVCO", "QRHC", "BHM", "FGEN", "GLOO", "APLT", "TLYS",
    "CNVS", "OPHC", "CLNN", "ACRV", "SLND", "BTM", "NRXP", "CUE", "RNXT", "AMPG",
    "VERU", "GEG", "HBIO", "GROV", "TEAD", "BDSX", "KORE", "FGBI", "PRTS", "TRT",
    "LTRN", "SABS", "GROW", "ACCS", "CELU", "CAMP", "XTNT", "RFL", "ZYXI", "IPWR",
    "VTVT", "ICCC", "HOWL", "BAFN", "BEEM", "CRWS", "GWH", "DIT", "NUKK", "TOON",
    "INMB", "BOF", "CVU", "TPCS", "SYPR", "WOLF", "IROQ", "SURG", "BRFH", "NOTV",
    "SNTI", "LITS", "KTCC", "VATE", "TUSK", "SKLZ", "GBIO", "LPSN", "SOTK", "FARM",
    "SCOR", "ANTX", "FEAM", "RMTI", "SCYX", "FLUX", "KSCP", "SLNG", "PDSB", "BODI",
    "BIRD", "OMCC", "MYO", "MHH", "SOHO", "SKYE", "HHS", "NERV", "LASE", "KOSS",
    "JOB", "ECOR", "NXTC", "IPSC", "FTHM", "DTI", "MAIA", "BRLT", "KLXE", "RVPH",
    "CSAI", "POCI", "NOTE", "JFB", "MKTW", "PASG", "RDI", "SCWO", "CVV", "NEPH",
    "DXR", "FEMY", "CPIX", "LEE", "MBBC", "AIRT", "HIT", "ANEB", "LNZA", "NTRB",
    "IBIO", "NMTC", "AHT", "DAIO", "NAII", "BZFD", "AIFF", "ESLA", "UONEK", "CRD.A",
    "ARTV", "DYAI", "XLO", "LESL", "NTIP", "SER", "VRAR", "BOLD", "INKT", "UG",
    "TZUP", "TBHC", "REFR", "SIDU", "DTST", "ZEO", "CTOR", "TCBS", "PXED", "LPCN",
    "CREX", "ELUT", "VVOS", "BELFA", "CODX", "BDL", "ATHA", "BEAT", "MLSS", "GTIM",
    "DARE", "CLIR", "BYSI", "SDST", "LIVE", "NIXX", "LGL", "NNVC", "WVVI", "TXMD",
    "AGH", "RLYB", "QTTB", "JRSH", "CCEL", "TCI", "LSTA", "ARKR", "PPSI", "USEG",
    "KPLT", "HFBL", "IRIX", "MXC", "LNAI", "FCUV", "BRID", "TOMZ", "PED", "AYTU",
    "SWAG", "AUID", "MSAI", "LSF", "RVP", "MODD", "TPST", "TVGN", "MGRX", "GOCO",
    "FLNT", "GENK", "SGRP", "UHG", "LOCL", "CVKD", "RENT", "BRN", "MTEX", "CRIS",
    "RAVE", "ASPSW", "TLF", "RBOT", "NINE", "UBCP", "OSTX", "MPLT", "BCG", "IPM",
    "NCSM", "SMXT", "ASST", "ASPSZ", "BATL", "LGVN", "ANY", "CISO", "COCH", "VGAS",
    "MRKR", "CXAI", "HYFM", "LVLU", "MOBX", "FBLG", "DLPN", "NVNO", "AMS", "SYBX",
    "COCP", "BTOC", "BIVI", "XOS", "CING", "KALA", "VEEA", "ISPO", "FUSB", "INLX",
    "SIF", "GIFT", "PIII", "AIRE", "PODC", "TAIT", "CLRB", "IPW", "NRXS", "WKSP",
    "JCTC", "SNYR", "BNAI", "FAT", "BFRG", "ELSE", "FLYX", "MIRA", "AGAE", "NXGL",
    "LYRA", "ACFN", "COHN", "KFFB", "AMOD", "SST", "NSYS", "INAB", "GLBZ", "XAIR",
    "IMNN", "MPTI.WS", "BNKK", "FGNX", "UONE", "RGS", "RMCO", "JUNS", "SHFS", "RYM",
    "KITT", "MSS", "FATBB", "ERNA", "SNAL", "MTVA", "NXPL", "VIVK", "IQST", "NYC",
    "ATLN", "YHGJ", "DRCT", "AXIL", "CKX", "CETY", "SNES", "DWSN", "SQFTW", "ADTI",
    "ADGM", "CJMB", "GTN.A", "LGL.WS", "2223637D", "SBT", "RLMT", "ARAV", "BTCSP", "NOVS",
    "HYZN"
]

# API settings
# NOTE: Grok has different rate limits than Claude
# Adjust these based on your actual rate limit experience
MAX_RETRIES = 5  # Increased retries
RETRY_DELAY = 120  # Wait 2 minutes on retry
REQUEST_DELAY = 10  # 10 seconds between requests


# ============================================================================
# MAIN CODE
# ============================================================================

def setup_data_directory():
    """Create the data directory if it doesn't exist"""
    Path(DATA_DIR).mkdir(exist_ok=True)
    print(f"✓ Data directory ready: {DATA_DIR}/")


def check_api_key():
    """Verify that the API key is set"""
    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        print("ERROR: XAI_API_KEY environment variable not set")
        print("\nTo set it:")
        print("  Mac/Linux: export XAI_API_KEY='your-key-here'")
        print("  Windows (PowerShell): $env:XAI_API_KEY='your-key-here'")
        print("  Windows (CMD): set XAI_API_KEY=your-key-here")
        exit(1)
    print("✓ API key found")
    return api_key


def generate_company_data(client, ticker):
    """
    Generate company data for a single ticker using Grok API
    
    Args:
        client: OpenAI client instance configured for xAI
        ticker: Stock ticker symbol
        
    Returns:
        dict: Company data or None if failed
    """
    prompt = YOUR_PROMPT.format(ticker=ticker)
    
    for attempt in range(MAX_RETRIES):
        try:
            print(f"  Requesting data for {ticker}... ", end="", flush=True)
            
            response = client.chat.completions.create(
                model="grok-4-1-fast-reasoning",
                messages=[
                    {
                        "role": "system",
                        "content": "You have access to real-time information. Provide comprehensive, accurate analysis with verified financial data from reliable sources. Only report events and dates that have actually occurred."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=8000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Filter out any thinking process if present
            # Grok may include reasoning steps, we only want the final report
            if "I'll conduct" in content or "Let me search" in content:
                # Try to extract just the report section
                lines = content.split('\n')
                filtered_lines = []
                skip_thinking = True
                
                for line in lines:
                    # Look for report start indicators
                    if any(indicator in line.lower() for indicator in ['# ', '## ', 'company overview', 'executive summary', 'sell-side']):
                        skip_thinking = False
                    
                    if not skip_thinking:
                        filtered_lines.append(line)
                
                if filtered_lines:
                    content = '\n'.join(filtered_lines)
            
            # Add disclaimer at the top
            disclaimer = """**Disclaimer:** This sell-side report was generated using Grok 4.1 Fast Reasoning (grok-4-1-fast-reasoning). Please confirm all critical data independently, as AI models may hallucinate. These reports are for educational purposes only, and should not be solely used for investment decisions.

Grok's API is currently limited to information up to the **end of 2024**. Claude's Sonnet 4.5 has access to up-to-date information, but is considerably more expensive per output (nearly $1 per ticker). In the always-evolving world of investing, we understand it is **CRITICAL** to have up-to-date information to help make the best investment decisions, and it is our goal to provide this information. But considering there are thousands of companies that we would ideally be updating monthly, as well as future goals of also providing quick and digestible summaries and insights for newly released earnings and conference calls, breaking news, FED speeches, etc, this quickly becomes very costly.

For this reason, please consider **subscribing to our Patreon** or donating to enable QuickTick AI to provide as much value and up-to-date insight as possible to **allow you to make the most informed investment decisions with a level of efficiency not possible even a few years ago.** 100% of the funds will go straight to purchasing more API credits to continue expanding our high quality, up-to-date analysis for more and more companies, and further then into our future value-generating plans. Thanks! - QuickTick AI

---

"""
            content = disclaimer + content
            
            print("✓")
            
            return {
                "ticker": ticker,
                "content": content,
                "generated_date": datetime.now().isoformat(),
                "model": "grok-4-1-fast-reasoning"
            }
            
        except Exception as e:
            error_msg = str(e)
            print(f"✗ (Attempt {attempt + 1}/{MAX_RETRIES})")
            print(f"    Error: {error_msg}")
            
            # Check if it's a rate limit error
            is_rate_limit = "rate_limit" in error_msg.lower() or "429" in error_msg
            
            if is_rate_limit:
                print(f"    Rate limit hit - waiting longer before retry")
            
            if attempt < MAX_RETRIES - 1:
                # Use exponential backoff for rate limits
                wait_time = RETRY_DELAY * (2 ** attempt) if is_rate_limit else RETRY_DELAY
                print(f"    Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"    Failed after {MAX_RETRIES} attempts")
                print(f"    Skipping {ticker} - you can re-run just this ticker later")
                return None


def save_company_data(data, ticker):
    """Save company data to a JSON file"""
    if data is None:
        return False
        
    filepath = Path(DATA_DIR) / f"{ticker}.json"
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"  Error saving {ticker}: {str(e)}")
        return False


def main():
    """Main execution function"""
    print("=" * 60)
    print("QUICK TICK - DATA GENERATOR (GROK)")
    print("=" * 60)
    print()
    
    # Setup
    setup_data_directory()
    api_key = check_api_key()
    
    # Initialize OpenAI client with xAI endpoint
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"
    )
    
    print(f"\nProcessing {len(TICKERS)} tickers...")
    print("=" * 60)
    
    # Statistics
    successful = 0
    failed = 0
    start_time = time.time()
    
    # Process each ticker
    for i, ticker in enumerate(TICKERS, 1):
        print(f"\n[{i}/{len(TICKERS)}] Processing {ticker}:")
        
        # Generate data
        data = generate_company_data(client, ticker)
        
        # Save data
        if save_company_data(data, ticker):
            print(f"  Saved to {DATA_DIR}/{ticker}.json")
            successful += 1
        else:
            failed += 1
        
        # Rate limiting - wait between requests
        if i < len(TICKERS):
            time.sleep(REQUEST_DELAY)
    
    # Final statistics
    elapsed_time = time.time() - start_time
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total time: {elapsed_time:.1f} seconds ({elapsed_time/60:.1f} minutes)")
    print(f"Average time per ticker: {elapsed_time/len(TICKERS):.1f} seconds")
    print()
    print(f"Data saved to: {Path(DATA_DIR).absolute()}")
    print()


if __name__ == "__main__":
    main()
