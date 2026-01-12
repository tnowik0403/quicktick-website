"""
QuickTick AI - Daily Update Buckets

91 daily buckets for quarterly rolling updates.
Total: 3486 companies
Evenly distributed: 38-39 tickers per day

Usage:
    from daily_buckets import get_bucket
    todays_tickers = get_bucket(1)  # Day 1
"""

DAILY_BUCKETS = [
    # Day 1 - 39 tickers
    [
        "AVGO", "META", "BRK.B", "LLY", "JPM", "JNJ", "XOM", "WMT", "NFLX", "COST",
        "ABBV", "HD", "PG", "BAC", "GE", "UNH", "CVX", "IBM", "WFC", "CSCO",
        "CAT", "MRK", "KO", "PM", "GS", "RTX", "ABT", "TMO", "MCD", "PEP",
        "LRCX", "LIN", "DIS", "AMGN", "UBER", "QCOM", "NEE", "AXP", "INTU",
    ],

    # Day 2 - 39 tickers
    [
        "APH", "TJX", "C", "INTC", "BKNG", "GILD", "VZ", "SPGI", "KLAC", "TXN",
        "BSX", "APP", "PFE", "DHR", "BLK", "BA", "COF", "WELL", "UNP", "LOW",
        "ADBE", "ETN", "ADI", "SYK", "HON", "DE", "PLD", "CEG", "CB", "VRTX",
        "COP", "MCK", "PH", "BX", "LMT", "CVS", "CME", "SO", "BMY",
    ],

    # Day 3 - 39 tickers
    [
        "NEM", "MO", "SBUX", "CMCSA", "DUK", "TMUS", "TT", "MMM", "MMC", "ICE",
        "WM", "ORLY", "CDNS", "HCA", "GD", "HWM", "NOC", "KKR", "CRH", "BK",
        "SNPS", "REGN", "SHW", "MRVL", "TDG", "USB", "ELV", "JCI", "EMR", "PNC",
        "MCO", "MDLZ", "WMB", "CI", "EQIX", "AON", "UPS", "ECL", "GM",
    ],

    # Day 4 - 39 tickers
    [
        "PWR", "ITW", "CMI", "COR", "DASH", "HLT", "TEL", "AEP", "MAR", "AZO",
        "TRV", "CSX", "NSC", "RCL", "GLW", "CL", "ADSK", "CTAS", "AJG", "SRE",
        "FCX", "MSI", "VST", "IDXX", "PYPL", "TFC", "AFL", "MPC", "EOG", "STX",
        "COIN", "FDX", "APD", "SPG", "ROST", "WDC", "WBD", "ALL", "BDX",
    ],

    # Day 5 - 39 tickers
    [
        "PCAR", "PSX", "VLO", "DLR", "SLB", "D", "APO", "O", "URI", "LHX",
        "KMI", "MNST", "ZTS", "EW", "CAH", "EA", "BKR", "CVNA", "XEL", "CBRE",
        "ROP", "EXC", "NDAQ", "WDAY", "FAST", "CMG", "CTVA", "OKE", "AME", "ABNB",
        "CARR", "RSG", "A", "ETR", "PSA", "MET", "TTWO", "GWW", "AMP",
    ],

    # Day 6 - 39 tickers
    [
        "DHI", "YUM", "MPWR", "AIG", "DAL", "MSCI", "TGT", "FICO", "DELL", "AXON",
        "CCI", "VMC", "HIG", "PRU", "EQT", "EBAY", "TRGP", "MLM", "RMD", "IQV",
        "XYZ", "VTR", "PAYX", "ED", "KMB", "WEC", "KDP", "WAB", "OTIS", "NUE",
        "GEHC", "PCG", "FIX", "FIS", "XYL", "KEYS", "CPRT", "FISV", "UAL",
    ],

    # Day 7 - 39 tickers
    [
        "ACGL", "KVUE", "NRG", "ARES", "GRMN", "IR", "VRSK", "WTW", "OXY", "SNDK",
        "MTD", "EXPE", "MTB", "HUM", "ADM", "CSGP", "TSCO", "MCHP", "SYF", "FITB",
        "FANG", "AEE", "HPE", "ATO", "EXR", "RJF", "VICI", "HSY", "FSLR", "EXE",
        "EME", "IBKR", "CCL", "CBOE", "BIIB", "BR", "AWK", "EFX", "CINF",
    ],

    # Day 8 - 39 tickers
    [
        "STE", "FE", "CNP", "PPL", "AVB", "ODFL", "HBAN", "IRM", "DOV", "GIS",
        "PHM", "ES", "DXCM", "TEAM", "LDOS", "ULTA", "DTE", "DG", "WAT", "NTRS",
        "VLTO", "LEN", "DVN", "STLD", "TDY", "PODD", "HPQ", "HUBB", "OMC", "TPR",
        "RF", "EIX", "CMS", "BRO", "TROW", "EQR", "LH", "PPG", "WRB",
    ],

    # Day 9 - 39 tickers
    [
        "WSM", "CFG", "DLTR", "LYV", "NTAP", "JBL", "VRSN", "KHC", "DGX", "LVS",
        "PTC", "DRI", "SBAC", "IP", "EL", "NI", "CHD", "ON", "NVR", "TYL",
        "HAL", "KEY", "LULU", "WST", "EXPD", "CPAY", "CTRA", "ROL", "TRMB", "CNC",
        "ZBH", "STZ", "CDW", "PFG", "SW", "PKG", "LUV", "GPC", "FTV",
    ],

    # Day 10 - 39 tickers
    [
        "LNT", "IFF", "EVRG", "CHTR", "CHRW", "L", "SNA", "GDDY", "INCY", "PNR",
        "SMCI", "MKC", "ESS", "Q", "APTV", "TPL", "DOW", "IT", "HOLX", "DD",
        "TSN", "INVH", "J", "WY", "MAA", "LII", "COO", "ALB", "BBY", "TXT",
        "GEN", "ALLE", "KIM", "FFIV", "GPN", "MAS", "BALL", "RL", "JBHT",
    ],

    # Day 11 - 39 tickers
    [
        "BG", "AVY", "CLX", "EG", "IEX", "FOXA", "DECK", "UHS", "REG", "ZBRA",
        "AKAM", "DPZ", "CF", "TKO", "JKHY", "DOC", "LYB", "SOLV", "VTRS", "HII",
        "RVTY", "HST", "UDR", "NDSN", "BLDR", "AIZ", "BXP", "CPT", "SWK", "HAS",
        "NWSA", "IVZ", "PNW", "SJM", "FDS", "GL", "DAY", "ALGN", "TECH",
    ],

    # Day 12 - 39 tickers
    [
        "WYNN", "AES", "EPAM", "SWKS", "BAX", "ARE", "MRNA", "APA", "GNRC", "CRL",
        "CAG", "FRT", "PAYC", "BF.B", "NCLH", "POOL", "LW", "MOH", "MTCH", "MOS",
        "TAP", "HSIC", "FOX", "AOS", "ERIE", "BEN", "HRL", "MGM", "CPB", "PSKY",
        "DVA", "NWS", "T", "SCHW", "MDT", "AMT", "VRT", "ALNY", "F",
    ],

    # Day 13 - 39 tickers
    [
        "FERG", "WCN", "INSM", "LNG", "PEG", "KR", "FLUT", "SYY", "VEEV", "SOFI",
        "STT", "NTRA", "CIEN", "LPLA", "BRK.A", "PSTG", "RDDT", "CRDO", "MKL", "HEI.A",
        "K", "UTHR", "CW", "CASY", "ZM", "FWONK", "RKLB", "EXAS", "ILMN", "THC",
        "FTI", "HUBS", "SGI", "RBA", "RKT", "GWRE", "WWD", "AFRM", "TLN",
    ],

    # Day 14 - 39 tickers
    [
        "TWLO", "SSNC", "FTAI", "USFD", "NVT", "FCNCA", "TRU", "FN", "BWXT", "SUI",
        "BURL", "XPO", "DKNG", "JLL", "FNF", "RIVN", "PFGC", "NBIX", "CRS", "PINS",
        "APG", "WPC", "EWBC", "RS", "NLY", "ITT", "RBC", "EQH", "DOCU", "ATI",
        "CG", "RPM", "TOL", "ACM", "GGG", "CACI", "CSL", "OKTA", "OHI",
    ],

    # Day 15 - 39 tickers
    [
        "U", "MTZ", "RGLD", "DT", "MEDP", "LECO", "DKS", "RVMD", "WCC", "NXT",
        "KTOS", "Z", "GH", "BLD", "TW", "ROKU", "IONS", "RGA", "BBIO", "DTM",
        "UNM", "RNR", "NTNX", "WSO", "QXO", "WMS", "SF", "BJ", "EVR", "ENTG",
        "EHC", "GLPI", "TXRH", "ELAN", "MLI", "LAMR", "ASTS", "FHN", "SNX",
    ],

    # Day 16 - 39 tickers
    [
        "EXEL", "ALLY", "CCK", "AYI", "W", "MTSI", "WTRG", "ELS", "CLH", "AGNC",
        "PEN", "AA", "BMRN", "HL", "ENSG", "AR", "MDGL", "OKLO", "MANH", "SCI",
        "CDE", "MKSI", "OVV", "AVAV", "DCI", "CMA", "RMBS", "IOT", "BAH", "PR",
        "GMED", "ORI", "JAZZ", "SPXC", "AMH", "STRL", "DY", "NYT", "REXR",
    ],

    # Day 17 - 39 tickers
    [
        "WBS", "RNA", "AFG", "AIT", "ARMK", "SATS", "RRX", "EGP", "HLI", "OC",
        "FYBR", "PLNT", "OWL", "FLS", "BWA", "AAL", "IDCC", "OGE", "GTLS", "CNM",
        "RGEN", "TTEK", "HQY", "FIVE", "GME", "SSB", "CR", "RRC", "SEIC", "WTFC",
        "AHR", "WAL", "KNSL", "MOD", "CUBE", "ROIV", "UGI", "DINO", "HALO",
    ],

    # Day 18 - 39 tickers
    [
        "PRI", "CRBG", "JEF", "PCOR", "COLB", "ADC", "SNAP", "CTRE", "CART", "SFM",
        "OSK", "ATR", "AWI", "LAD", "COKE", "RBRK", "VMI", "CYTK", "BRX", "AVTR",
        "AEIS", "LYFT", "QRVO", "SANM", "ZION", "LNC", "NNN", "ONB", "G", "JOBY",
        "CNH", "LKQ", "ZWS", "UMBF", "AXS", "FR", "WTS", "SOLS", "OLLI",
    ],

    # Day 19 - 39 tickers
    [
        "CFR", "SAIA", "LUMN", "TPG", "NFG", "CLF", "ALSN", "WING", "MASI", "HIMS",
        "STAG", "OMF", "JBTM", "BPOP", "CADE", "EXP", "RYTM", "AMG", "DUOL", "HEI",
        "CMC", "AN", "EMN", "IDA", "CORT", "PNFP", "KNX", "BROS", "ONTO", "SSD",
        "ARWR", "FLR", "INGR", "CHDN", "TTC", "CHWY", "FND", "PTCT", "VFC",
    ],

    # Day 20 - 39 tickers
    [
        "JXN", "CBSH", "TTMI", "MAT", "VOYA", "AGCO", "R", "MUSA", "FSS", "GAP",
        "H", "MTG", "ORA", "AXTA", "PCTY", "MOG.A", "PRIM", "EAT", "TRNO", "ESAB",
        "PCVX", "AAON", "AXSM", "HR", "SMTC", "CHE", "STWD", "AL", "FAF", "VNO",
        "CWAN", "SNV", "LFUS", "KEX", "SEE", "DOCS", "RYAN", "EPRT", "IBP",
    ],

    # Day 21 - 39 tickers
    [
        "SITM", "PB", "FBIN", "VNOM", "CRUS", "TXNM", "BSY", "MHK", "EXLS", "NEU",
        "RITM", "HXL", "MIR", "AM", "IRTC", "CWST", "BIO", "CIFR", "SITE", "FCFS",
        "MSA", "THG", "ESI", "KD", "FNB", "AUR", "BOOT", "TMHC", "ESNT", "BFAM",
        "LIF", "GTES", "SLM", "MKTX", "COGT", "GXO", "KMX", "GKOS", "M",
    ],

    # Day 22 - 39 tickers
    [
        "NOV", "RDNT", "LEA", "RHP", "LAZ", "ULS", "FROG", "GATX", "KRYS", "ACI",
        "PIPR", "HRB", "PTGX", "WH", "POR", "RAL", "ARW", "NXST", "ESE", "NUVL",
        "DAR", "LBRDK", "CVLT", "COMP", "UEC", "JHG", "DBX", "MORN", "MIDD", "GTLB",
        "RLI", "CHRD", "VLY", "WFRD", "ENS", "OLED", "BKH", "SWX", "THO",
    ],

    # Day 23 - 39 tickers
    [
        "CDTX", "VNT", "KBR", "FCN", "UBSI", "BMI", "ACA", "GBCI", "CNX", "MTN",
        "GPI", "LMND", "BRKR", "ROAD", "UFPI", "LPX", "MMSI", "AGX", "TKR", "ETSY",
        "KRG", "QLYS", "WEX", "KRC", "OPCH", "BCPC", "TFX", "OGS", "GNTX", "HOMB",
        "WTM", "MTH", "SR", "OZK", "ALK", "ABCB", "ALKS", "HWC", "HLNE",
    ],

    # Day 24 - 39 tickers
    [
        "MMS", "ACIW", "CAVA", "AUB", "NJR", "OPEN", "RDN", "POST", "GPK", "SIGI",
        "TGTX", "MC", "MTDR", "QS", "TMDX", "APPF", "PRAX", "MRP", "NPO", "FOUR",
        "CVCO", "GVA", "ECG", "BILL", "BYD", "SBRA", "ST", "CORZ", "URBN", "SKY",
        "CZR", "WK", "UHAL.B", "CE", "CSW", "ABG", "WULF", "CCC", "PSN",
    ],

    # Day 25 - 39 tickers
    [
        "LSTR", "ITRI", "TTAN", "PI", "AMKR", "BDC", "ADT", "HRI", "PECO", "ANF",
        "BCO", "LOPE", "REZI", "RUN", "AX", "MAC", "CROX", "VSAT", "MDU", "ADMA",
        "MUR", "BC", "SPR", "OSIS", "CUZ", "WHR", "LEU", "QTWO", "CRNX", "ACHR",
        "HASI", "STEP", "HUT", "NWE", "RIG", "FORM", "KNF", "TNL", "LEN.B",
    ],

    # Day 26 - 39 tickers
    [
        "WAY", "AMTM", "SON", "ATMU", "SXT", "MARA", "AKRO", "COMM", "ASB", "KTB",
        "BTSG", "HCC", "TCBI", "DLB", "ELF", "AROC", "NOVT", "AGO", "MGY", "FLG",
        "PVH", "BOX", "SAIC", "EBC", "CLSK", "ACLX", "SNEX", "IRT", "LNTH", "VIAV",
        "MSGS", "SLAB", "EPR", "VVV", "AVT", "MSM", "FTDR", "VSEC", "VKTX",
    ],

    # Day 27 - 39 tickers
    [
        "SIG", "SIRI", "ALE", "HAE", "WMG", "CNR", "PRM", "CELC", "LAUR", "SKYW",
        "BRBR", "NE", "LLYVK", "PJT", "KYMR", "PLXS", "CWK", "PFSI", "FFIN", "PRMB",
        "OSCR", "MWA", "MRCY", "CNO", "LGND", "FHI", "TREX", "BHF", "IESC", "ZG",
        "VCYT", "KBH", "TDS", "IBOC", "UCB", "LTH", "BBWI", "INSP", "EXPO",
    ],

    # Day 28 - 39 tickers
    [
        "DORM", "SKT", "SRRK", "INDB", "FELE", "NHI", "ENPH", "PII", "GNW", "VRNS",
        "GPOR", "SFBS", "ICUI", "SHC", "NVST", "CDP", "MHO", "PATK", "OTTR", "RYN",
        "KFY", "APGE", "CALM", "WSC", "HAYW", "CRC", "SLGN", "GRAL", "GHC", "SLG",
        "RNST", "YETI", "VCTR", "AVA", "KVYO", "SHAK", "OUT", "CBT", "ARQT",
    ],

    # Day 29 - 38 tickers
    [
        "MYRG", "VRRM", "FULT", "MATX", "KAI", "ZETA", "CPK", "BKU", "BRC", "CALX",
        "VAL", "PSMT", "ASO", "ALGM", "MZTI", "YOU", "TENB", "AEO", "BGC", "PLMR",
        "ATGE", "BL", "CATY", "RARE", "BNL", "BXMT", "FBP", "ACAD", "UUUU", "SPSC",
        "TVTX", "GFF", "FUL", "BTU", "ENVA", "WGS", "VSCO", "TGNA",
    ],

    # Day 30 - 38 tickers
    [
        "POWL", "MIRM", "WSFS", "AAP", "AGYS", "COLD", "CGON", "FHB", "AIR", "GSAT",
        "TPC", "HGV", "FOLD", "SHOO", "SARO", "DOCN", "TARS", "MGEE", "HIW", "CBU",
        "AZZ", "BFH", "HOG", "RRR", "PCH", "IDYA", "SXI", "NMIH", "WSBC", "DAN",
        "WHD", "PBH", "LOAR", "EEFT", "VIRT", "TEX", "CPRI", "RUSHA",
    ],

    # Day 31 - 38 tickers
    [
        "BCC", "CNK", "HURN", "CARG", "ADPT", "AWR", "WU", "TPH", "VC", "VRDN",
        "AVNT", "TBBK", "FRPT", "DYN", "PBF", "APAM", "SBCF", "FIBK", "BLKB", "LBRT",
        "FRSH", "CWEN", "CXT", "LXP", "NSIT", "DRS", "NATL", "CPRX", "CIVI", "KGS",
        "KAR", "PRVA", "CWT", "PL", "AKR", "ABM", "SFNC", "HHH",
    ],

    # Day 32 - 38 tickers
    [
        "WDFC", "ALHC", "PTON", "PAG", "LRN", "RHI", "BOH", "INSW", "LCII", "KSS",
        "MPW", "ACLS", "MCY", "NCNO", "UNF", "TDC", "CVBF", "ONDS", "MGRC", "BKD",
        "ITGR", "APLE", "GTM", "CRWV", "ATEC", "CBZ", "DAVE", "FCPT", "SYNA", "HP",
        "CON", "BOKF", "WAFD", "REVG", "UPWK", "INTA", "LINE", "JOE",
    ],

    # Day 33 - 38 tickers
    [
        "DNOW", "ALRM", "HWKN", "XMTR", "OII", "NMRK", "SMG", "SUPN", "OLN", "IRON",
        "MTRN", "KMPR", "UE", "FBK", "ASH", "SLNO", "PLUS", "PFS", "RH", "DXC",
        "GT", "IAC", "EWTX", "PLUG", "DNLI", "BANC", "CHH", "TOWN", "BEAM", "COCO",
        "RNG", "APLS", "TDW", "XRAY", "CURB", "FFBC", "HI", "ATKR",
    ],

    # Day 34 - 38 tickers
    [
        "PRK", "CHEF", "HUBG", "RELY", "NUVB", "SPHR", "KRMN", "EXTR", "DK", "PARR",
        "ADUS", "GOLF", "TERN", "IVT", "FWONA", "AMRX", "SM", "CSGS", "RXO", "EYE",
        "PENN", "TRN", "CAR", "STC", "UNFI", "PTEN", "BBT", "WLK", "MLYS", "CAKE",
        "SONO", "BRZE", "GEO", "AORT", "MGNI", "TRMK", "KMT", "LQDA",
    ],

    # Day 35 - 38 tickers
    [
        "MD", "WD", "CUBI", "CACC", "OI", "GRBK", "NOG", "LEVI", "VICR", "CRVL",
        "AVPT", "RCUS", "SPNT", "BANR", "TXG", "FLO", "PGNY", "NBTB", "EPAC", "HE",
        "DIOD", "BANF", "OCUL", "SYRE", "SEI", "NSA", "VCEL", "FRME", "NWN", "FBNC",
        "PHIN", "OLMA", "OGN", "SMMT", "SRPT", "BUSE", "AVDL", "NNI",
    ],

    # Day 36 - 38 tickers
    [
        "WRBY", "HCI", "LC", "ARR", "CRK", "DEI", "BWIN", "DDS", "CNXC", "CC",
        "NGVT", "KWR", "EFSC", "MSGE", "CTRI", "RXRX", "SYBT", "MQ", "POWI", "ASGN",
        "HMN", "QDEL", "DRH", "EVTC", "IOSP", "DX", "IPGP", "CLDX", "NTCT", "MTX",
        "PK", "PRGO", "TWST", "CXW", "LION", "SDRL", "PPC", "HLIO",
    ],

    # Day 37 - 38 tickers
    [
        "HNI", "RAMP", "FMC", "SMPL", "PRGS", "SKWD", "CNS", "SHO", "BELFB", "OFG",
        "GEF", "DJT", "DBRG", "GNL", "NWBI", "KN", "VECO", "VERA", "NTST", "CCS",
        "HUN", "IE", "HRMY", "BKE", "YELP", "ENOV", "GSHD", "HLMN", "TNET", "CASH",
        "SNDX", "VAC", "ATRC", "ATRO", "NHC", "LMAT", "AGIO", "SCS",
    ],

    # Day 38 - 38 tickers
    [
        "VSH", "CHCO", "IMVT", "CRGY", "STRA", "LTC", "ACMR", "PAYO", "LCID", "PRCT",
        "AMR", "ANDE", "RSI", "UFPT", "KNSA", "ALG", "BLBD", "WOR", "OS", "SEM",
        "PRDO", "SLVM", "TPB", "GTY", "LZ", "LZB", "STOK", "FLYW", "FCF", "AAOI",
        "OMCL", "LASR", "CLMT", "SBH", "CENTA", "STBA", "ANIP", "CECO",
    ],

    # Day 39 - 38 tickers
    [
        "BATRK", "NEO", "MNKD", "CENX", "TRIP", "ELME", "DBD", "SAM", "FSLY", "AGM",
        "TILE", "ROG", "NWL", "MODG", "BHE", "PBI", "HTH", "ACHC", "BCRX", "LLYVA",
        "KNTK", "NIC", "IRDM", "KALU", "ABR", "CWEN.A", "HTO", "ROCK", "DGII", "DV",
        "IMNM", "WT", "JJSF", "WERN", "ARLO", "XPRO", "ICFI", "DNTH",
    ],

    # Day 40 - 38 tickers
    [
        "PCT", "LKFN", "STEL", "FIVN", "AMLX", "IPAR", "ARI", "CCB", "PAY", "TALO",
        "COLL", "TNDM", "NBHC", "AIN", "AZTA", "WLDN", "ZYME", "MBC", "PAR", "UPB",
        "SHLS", "ARCB", "WLY", "IIPR", "FDP", "VERX", "FUN", "NSSC", "HCSG", "SPB",
        "VVX", "NVCR", "TRVI", "TIC", "NVRI", "DVAX", "NRIX", "MAN",
    ],

    # Day 41 - 38 tickers
    [
        "TNC", "HOUS", "CNMD", "PEB", "ZD", "TDOC", "COLM", "GABC", "XHR", "EFC",
        "REAL", "SGRY", "ALKT", "JANX", "JBLU", "ARDX", "VYX", "GBX", "LEG", "SILA",
        "PLAB", "HROW", "PZZA", "WINA", "QCRH", "REYN", "INVA", "RLAY", "NEOG", "DCO",
        "PACS", "TCBK", "HOPE", "WEN", "FLNC", "ADEA", "ACVA", "AMC",
    ],

    # Day 42 - 38 tickers
    [
        "LADR", "DFIN", "TRS", "NKTR", "LNN", "FIGR", "UVV", "AXGN", "WWW", "CTS",
        "HLF", "ENR", "PRLB", "PRA", "MCRI", "PGRE", "MBX", "TFIN", "XNCR", "BBNX",
        "DCOM", "AAMI", "WKC", "MXL", "USLM", "CNOB", "CDRE", "WABC", "ALGT", "BF.A",
        "ATEN", "NSP", "PFBC", "CMPR", "BFC", "DXPE", "SVRA", "TNGX",
    ],

    # Day 43 - 38 tickers
    [
        "BLFS", "HSII", "COTY", "PHR", "UMH", "JBGS", "FTRE", "ARRY", "THR", "WS",
        "LGN", "ECPG", "ACT", "TRUP", "ALEX", "UTI", "CSR", "EYPT", "NEXT", "USPH",
        "SEB", "UWMC", "IMKTA", "VITL", "CERT", "PMT", "CRI", "SION", "CRAI", "ASAN",
        "PDM", "LOB", "PRG", "UCTT", "FA", "NVAX", "OBK", "RLJ",
    ],

    # Day 44 - 38 tickers
    [
        "AMRC", "VRE", "SAFT", "FWRG", "SDGR", "COHU", "GIII", "EZPW", "MLKN", "PWP",
        "KURA", "TWO", "XERS", "FUBO", "PD", "SEZL", "DHC", "CSTL", "CVI", "HLIT",
        "OCFC", "ASTH", "VRTS", "TSHA", "GO", "NN", "JAMF", "XPEL", "SAIL", "LGIH",
        "THS", "IAS", "PCRX", "PENG", "KW", "GRC", "ORKA", "WTTR",
    ],

    # Day 45 - 38 tickers
    [
        "ASTE", "INVX", "MFA", "ORC", "PEBO", "EXPI", "IDT", "MAZE", "PRO", "ECVT",
        "ORIC", "OSBC", "THRM", "ALIT", "PRKS", "CIM", "AHCO", "AMPH", "EIG", "INBX",
        "SCL", "RVLV", "NTLA", "RPD", "WGO", "SRCE", "ELVN", "LUNR", "ALH", "ESRT",
        "NPKI", "PHAT", "PRCH", "PVLA", "GBTG", "CLOV", "SNDR", "DEA",
    ],

    # Day 46 - 38 tickers
    [
        "TTI", "ESPR", "MSEX", "HLX", "STAA", "SAH", "REX", "VTOL", "CDNA", "UNIT",
        "AAT", "DLX", "COUR", "UVSP", "WMK", "AVBP", "CCOI", "CTBI", "BV", "CXM",
        "UTL", "ZBIO", "ROOT", "UPBD", "RAPP", "SMA", "BETA", "NTSK", "ARVN", "PDFS",
        "IART", "BBSI", "GLUE", "SEPN", "MEG", "PNTG", "RIGL", "FBRT",
    ],

    # Day 47 - 38 tickers
    [
        "YEXT", "IAUX", "TMP", "UVE", "PAHC", "RAPT", "DRVN", "AMPL", "SBSI", "ANAB",
        "FMBH", "BHRB", "HAFC", "HFWA", "EPC", "FIGS", "SMP", "GLDD", "HBNC", "JBI",
        "SCSC", "IOVA", "ODP", "BJRI", "VSTM", "NAVI", "TFSL", "PUMP", "ALNT", "FIZZ",
        "SIBN", "DAKT", "AD", "CMP", "KOD", "AMWD", "CNNE", "AIV",
    ],

    # Day 48 - 38 tickers
    [
        "PRSU", "GLIBK", "PLYM", "BCAX", "TRST", "IRMD", "LENZ", "BY", "TBPH", "LFST",
        "NBBK", "QNST", "ERII", "CPF", "MDXG", "LBRDA", "RHLD", "HPP", "MCB", "SLDP",
        "RZLT", "SAFE", "AMTB", "EMBC", "CFFN", "SNCY", "ESQ", "EVER", "ERAS", "LMB",
        "METC", "AMSF", "TDUP", "DAWN", "NTGR", "CCNE", "RWT", "BRSP",
    ],

    # Day 49 - 38 tickers
    [
        "MBWM", "VSTS", "MIAX", "GOSS", "GERN", "MATW", "MMI", "VIR", "EQBK", "AXL",
        "JBSS", "PLOW", "BLND", "APOG", "TDAY", "SANA", "BFST", "UA", "CMPX", "NIQ",
        "FWRD", "VG", "NBR", "RCAT", "CARS", "AVAH", "CNXN", "IBRX", "SEMR", "UAA",
        "BZH", "ABUS", "HRTG", "BBW", "IBCP", "MBIN", "MYGN", "ADAM",
    ],

    # Day 50 - 38 tickers
    [
        "MYE", "UTZ", "KE", "RUSHB", "HNGE", "CTLP", "PACB", "ORRF", "GDOT", "TYRA",
        "CRMD", "CAC", "TR", "KALV", "WSR", "FG", "UFCS", "AQST", "MATV", "CWH",
        "CBRL", "CBL", "HTZ", "CTMX", "VTYX", "GPRE", "AESI", "AMN", "CGEM", "HTBK",
        "AEHR", "DJCO", "MOFG", "NRDS", "FULC", "ADTN", "EE", "RYI",
    ],

    # Day 51 - 38 tickers
    [
        "UAMY", "OMER", "OPY", "GES", "RBCAA", "HYMC", "ANNX", "TREE", "THFF", "NX",
        "MPB", "SG", "NXRT", "CTKB", "HNRG", "ACEL", "CMPO", "TRTX", "VTS", "RGNX",
        "HTB", "SABR", "MTUS", "PRAA", "RUM", "HSTM", "INDI", "BW", "OFIX", "GHM",
        "PX", "PSNL", "BOW", "FLGT", "SENEA", "ALMS", "GSBC", "NAVN",
    ],

    # Day 52 - 38 tickers
    [
        "HOV", "NBN", "PGEN", "CRVS", "CTEV", "FISI", "CCO", "MRTN", "SBGI", "AIOT",
        "EBS", "BDN", "IVVD", "CSV", "SMBC", "ETD", "STGW", "INN", "CASS", "ATXS",
        "CTO", "KOP", "NABL", "DFH", "SHEN", "IIIN", "HIPO", "WASH", "CCBG", "LQDT",
        "SXC", "FOXF", "VTLE", "GDEN", "GDYN", "LINC", "ODC", "OXM",
    ],

    # Day 53 - 38 tickers
    [
        "LXEO", "ICHR", "TCMD", "NWPX", "FCBC", "IIIV", "IVR", "SMBK", "ASPI", "YORW",
        "REPL", "CWCO", "NRIM", "CEVA", "MBUU", "UHT", "KFRC", "HGTY", "SHBI", "EGBN",
        "APEI", "FDMT", "KODK", "RES", "GRDN", "SPRY", "MNRO", "CABO", "AVNS", "UHAL",
        "BLMN", "GOGO", "FFIC", "BFLY", "ARHS", "CPS", "HTFL", "OPK",
    ],

    # Day 54 - 38 tickers
    [
        "BLLN", "AHH", "FSBC", "MCW", "IDR", "LYTS", "PLPC", "SSTK", "NPK", "CLB",
        "TRNS", "GOOD", "GOLD", "OPTU", "BXC", "MH", "BWMN", "AVO", "MCBS", "MAGN",
        "SPT", "SCHL", "CODI", "UDMY", "TROX", "APPS", "GEVO", "GCMG", "PKST", "AMAL",
        "FMNB", "AOSL", "IRWD", "SKYT", "TE", "ANGO", "FSUN", "AROW",
    ],

    # Day 55 - 38 tickers
    [
        "HIFS", "VREX", "ALX", "BCAL", "FOR", "RGR", "CBLL", "SERV", "BKV", "SPFI",
        "EVH", "ARX", "ALT", "NUS", "NLOP", "NAGE", "CYRX", "DIN", "GTN", "PLAY",
        "KREF", "URG", "MRVI", "COFS", "JBIO", "BHB", "ZVRA", "LXU", "LIND", "CMCO",
        "AXTI", "ALRS", "ACNB", "PSIX", "FIP", "NP", "HZO", "OSPN",
    ],

    # Day 56 - 38 tickers
    [
        "IMXI", "SD", "MLR", "NPB", "XOMA", "SFIX", "CYH", "TCBX", "CLBK", "SLDE",
        "HELE", "NPCE", "BSRR", "EHAB", "ANGI", "EBF", "IHRT", "NFBK", "AIP", "PFIS",
        "LAB", "PGC", "ABSI", "TIPT", "IBTA", "GMRE", "RXST", "CLMB", "DC", "CARE",
        "MLAB", "CHCT", "CIVB", "WRLD", "RYAM", "EVGO", "LYEL", "GRPN",
    ],

    # Day 57 - 38 tickers
    [
        "TALK", "AKBA", "VPG", "OSG", "VIA", "SWIM", "MNPR", "FRBA", "CMTG", "FBIZ",
        "CCSI", "FFWM", "SFST", "DNA", "RC", "WEAV", "REPX", "SES", "EOLS", "ZEUS",
        "CLPT", "ASIX", "FRGE", "CAL", "ULCC", "GCO", "NUTX", "ZUMZ", "OCGN", "GRND",
        "BMRC", "FPI", "IMRX", "TWI", "CWBC", "GIC", "MAMA", "ASMB",
    ],

    # Day 58 - 38 tickers
    [
        "BFS", "FLY", "BAND", "MITK", "MTW", "TITN", "EVEX", "ORN", "NXDR", "KOPN",
        "KRNY", "OIS", "KMTS", "ENTA", "EGY", "HBCP", "ITIC", "JACK", "PKE", "ETON",
        "NGVC", "PUBM", "SWBI", "BETR", "CTOS", "PRME", "SITC", "DOMO", "WTBA", "MAX",
        "MCS", "FET", "NGS", "CLNE", "TWFG", "HTLD", "BGS", "BWB",
    ],

    # Day 59 - 38 tickers
    [
        "SVV", "OLP", "DGICA", "GRNT", "UNTY", "TRC", "BIOA", "CLFD", "CVGW", "WNC",
        "MBI", "MGPI", "PSTL", "PTLO", "LXFR", "ANRO", "BCML", "PTRN", "DNUT", "MSBI",
        "GLRE", "AVBC", "KROS", "BOC", "BBBY", "ORGO", "GBFH", "ABAT", "ABL", "SOC",
        "ILPT", "CCRN", "SLDB", "LCTX", "DHIL", "CERS", "HVT", "LAND",
    ],

    # Day 60 - 38 tickers
    [
        "RBB", "FSBW", "CLDT", "XRX", "PDLB", "CBNK", "MOV", "RDW", "AVXL", "FLOC",
        "TBRG", "ATLC", "TRDA", "ALDX", "NRC", "BYRN", "BNC", "BATRA", "CRSR", "STRT",
        "AURA", "MVBF", "EAF", "NVEC", "MTRX", "ACCO", "ZIP", "DCTH", "CVLG", "VENU",
        "DENN", "VLGEA", "VNDA", "KRUS", "LPTH", "KIDS", "MCFT", "NCMI",
    ],

    # Day 61 - 38 tickers
    [
        "SMC", "IPI", "FVR", "CBAN", "CDZI", "MEC", "TLS", "RCKT", "RM", "CMRC",
        "SCVL", "CNDT", "SLP", "SMRT", "QTRX", "SSP", "HBT", "PEPG", "CZNC", "BWFG",
        "FMAO", "PCB", "SNWV", "DSGN", "ACRS", "VOYG", "HY", "MVIS", "CLW", "SVC",
        "HLLY", "NEWT", "RRBI", "SGHT", "MG", "MCHB", "OOMA", "BRBS",
    ],

    # Day 62 - 38 tickers
    [
        "NATR", "AVTX", "ARTNA", "DSGR", "ACRE", "SMLR", "GNE", "TARA", "AMCX", "USCB",
        "CIA", "LOCO", "ONIT", "OBT", "FRPH", "DDD", "OPFI", "ARKO", "WNEB", "RNGR",
        "ASPN", "BMBL", "WSBF", "SRTA", "PLSE", "ATEX", "TOI", "TSBK", "WOW", "CIO",
        "KELYA", "FRST", "LXRX", "BNTC", "MBCN", "HDSN", "MEI", "ISTR",
    ],

    # Day 63 - 38 tickers
    [
        "BLFY", "RPAY", "XPER", "LMNR", "TH", "RMNI", "BVS", "PINE", "FBLA", "AVNW",
        "CZFS", "WLFC", "RBBN", "AII", "NECB", "CTRN", "ABEO", "GALT", "CBIO", "GDRX",
        "PKBK", "EGHT", "CRD.B", "RR", "HYLN", "JMSB", "HNST", "OPRX", "BALY", "TECX",
        "SNDA", "III", "FUNC", "WOOF", "ACHV", "LDI", "FNLC", "PYXS",
    ],

    # Day 64 - 38 tickers
    [
        "AVIR", "ALTS", "PLBC", "MPAA", "SIGA", "KYTX", "THRY", "FCCO", "ACIC", "FSTR",
        "NGNE", "FENC", "CTNM", "FRAF", "SPOK", "ALLO", "UMAC", "PACK", "RMR", "EGAN",
        "EFSI", "FBRX", "CABA", "XFOR", "MITT", "WEST", "USNA", "NFE", "RLGT", "LRMR",
        "QSI", "RCKY", "VABK", "VYGR", "JCAP", "CAPR", "MFIN", "PBYI",
    ],

    # Day 65 - 38 tickers
    [
        "CRCT", "PCYO", "EDIT", "NWFL", "PESI", "CFFI", "CHMG", "CVRX", "JELD", "SPCE",
        "AMPY", "TBCH", "REKR", "ELMD", "BRY", "NATH", "OVLY", "PKOH", "IMMR", "LFCR",
        "ATLO", "BPRN", "KRMD", "TG", "DOUG", "FVCB", "REFI", "FEIM", "JRVR", "ATNI",
        "BH", "INR", "MYFW", "OMI", "BLZE", "VMD", "TASK", "AGL",
    ],

    # Day 66 - 38 tickers
    [
        "NMRA", "CTGO", "SENS", "KRT", "ARDT", "ASUR", "SLQT", "CENT", "ASLE", "KFS",
        "CRBP", "HCAT", "LOVE", "ONTF", "CURI", "WEYS", "RICK", "HWBK", "GPRO", "SLS",
        "BKTI", "OWLT", "TWIN", "TSSI", "SPIR", "LCNB", "AREC", "GETY", "LPRO", "STRS",
        "FDBC", "BKKT", "BSVN", "TRAK", "SKYH", "EB", "LNKB", "INV",
    ],

    # Day 67 - 38 tickers
    [
        "QUAD", "PPIH", "CZWI", "MRBK", "CCCC", "UTMD", "FXNC", "NC", "TCX", "JOUT",
        "OPRT", "ALTO", "VTGN", "INFU", "CADL", "RGCO", "GYRE", "SDHC", "SGMT", "OPBK",
        "PAL", "HUMA", "LE", "MNTN", "VEL", "VUZI", "NKSH", "FFAI", "PEBK", "GEOS",
        "FC", "XPOF", "FLXS", "SMHI", "BVFL", "USAU", "UIS", "BHR",
    ],

    # Day 68 - 38 tickers
    [
        "KINS", "LAW", "FRMI", "PBFS", "TRUE", "BNED", "ASIC", "DBI", "HRTX", "CRBU",
        "ISBA", "GNLX", "AOMR", "INGN", "OMDA", "LEGH", "HPK", "IKT", "ECBK", "CHPT",
        "WTI", "DIBS", "PAYS", "DUOT", "OSUR", "ACR", "GEMI", "POWW", "EVC", "REI",
        "TNYA", "CBFV", "OBIO", "SEG", "SUIG", "ACTG", "FINW", "DSP",
    ],

    # Day 69 - 38 tickers
    [
        "MASS", "BDTX", "RMBI", "CRMT", "CHRS", "ARCT", "TTSH", "FTK", "FHTX", "RMAX",
        "BBCP", "FSFG", "PRTH", "MXCT", "SBFG", "FCEL", "ALCO", "FLD", "FOA", "BSET",
        "BRT", "GIFI", "LWAY", "RGP", "TAYD", "CRDF", "QNCX", "DVLT", "LTRX", "MRAM",
        "CMT", "GCBC", "OABI", "TTGT", "GSIT", "INBK", "SRI", "TNXP",
    ],

    # Day 70 - 38 tickers
    [
        "AGEN", "LODE", "CDXS", "STXS", "SKYX", "OVBC", "STRZ", "SMID", "MNSB", "ALTI",
        "SATL", "SAVA", "DMRC", "SAMG", "HNVR", "CATX", "TLSI", "GENC", "BFIN", "TGEN",
        "GPMT", "FOSL", "HOFT", "TBI", "INO", "STEM", "ONEW", "FNWD", "TMCI", "BTCS",
        "ANIK", "SRBK", "UBFO", "EBMT", "JAKK", "KLC", "FRD", "ANIX",
    ],

    # Day 71 - 38 tickers
    [
        "SNFCA", "SEVN", "LAKE", "QIPT", "SGC", "INSG", "WHG", "LARK", "DH", "AARD",
        "HBB", "XGN", "ISSC", "ONL", "ESCA", "SRG", "LFMD", "STEX", "VOR", "APYX",
        "EVI", "ARQ", "MBOT", "ALTG", "KLTR", "FONR", "BLNK", "JYNT", "MDV", "ELDN",
        "NAUT", "GWRS", "AREN", "ACNT", "AMBQ", "MRSN", "RELL", "INTT",
    ],

    # Day 72 - 38 tickers
    [
        "AVD", "MCRB", "SKIN", "ACU", "KVHI", "ELA", "ASYS", "FBYD", "SPWR", "KRO",
        "BOOM", "OVID", "RPT", "SRZN", "EWCZ", "KULR", "DFDV", "COYA", "BCBP", "MED",
        "PDEX", "FNKO", "OLPX", "SCLX", "EPM", "GLIBA", "JILL", "NREF", "FATE", "ULH",
        "NXDT", "ALEC", "ARAY", "MPTI", "MLP", "AOUT", "EHTH", "SUNS",
    ],

    # Day 73 - 38 tickers
    [
        "SNBR", "CGTX", "AMTX", "IRD", "CFBK", "INNV", "RVSB", "KEQU", "NPWR", "HURA",
        "CARL", "CNTX", "CLAR", "CHGG", "CSPI", "ZVIA", "HAIN", "RAIL", "EML", "STHO",
        "MNTK", "HURC", "CCLD", "RCMT", "HFFG", "UNCY", "VIRC", "LUCK", "AEYE", "EPSN",
        "ATOS", "RCEL", "ESOA", "SPRO", "SEER", "PLBY", "PEW", "MGNX",
    ],

    # Day 74 - 38 tickers
    [
        "QMCO", "GNSS", "AIRO", "GORO", "LGCY", "BARK", "PLRX", "LNSR", "FSP", "CBNA",
        "LUCD", "TYGO", "DCGO", "NVCT", "KG", "EXOD", "STRW", "FLL", "SRFM", "ELTX",
        "TTEC", "MPX", "INVE", "STTK", "SGMO", "PROV", "NKTX", "RPID", "FF", "MAPS",
        "GUTS", "GRWG", "CXDO", "EXFY", "CMTL", "QUIK", "CPSS", "ANVS",
    ],

    # Day 75 - 38 tickers
    [
        "NODK", "RSSS", "FORR", "OM", "VHC", "AXR", "HYPR", "RILY", "CRVO", "PMTS",
        "UNB", "SERA", "SND", "OFLX", "BMNR", "SPWH", "DERM", "AISP", "FNWB", "STIM",
        "DHX", "CHMI", "ADVM", "FDSB", "BRCC", "ALMU", "WRAP", "NRDY", "WWR", "SWKH",
        "CTM", "CHYM", "BTMD", "RXT", "BH.A", "BYND", "CLST", "ATOM",
    ],

    # Day 76 - 38 tickers
    [
        "NTIC", "ZNTL", "ACTU", "CHCI", "STRO", "AVBH", "RDNW", "IMMX", "METCB", "VRA",
        "LFVN", "RNAC", "SPRU", "ABOS", "ASRT", "WHWK", "APT", "SRTS", "ATYR", "FTLF",
        "BMEA", "AIRJ", "IZEA", "ESP", "PZG", "SMTI", "RRGB", "BWEN", "GLIBR", "FBIO",
        "ASPS", "PMVP", "ATRA", "QVCGA", "ULBI", "SSBI", "BOTJ", "DLHC",
    ],

    # Day 77 - 38 tickers
    [
        "CODA", "CYPH", "FTCI", "CATO", "LUNG", "CDLX", "ALOT", "HNNA", "FSI", "HGBL",
        "IMUX", "SSTI", "TSQ", "WYY", "NNBR", "OPAL", "CVGI", "TZOO", "LAZR", "CPBI",
        "MYPS", "PLCE", "AIRS", "UPLD", "FSEA", "OTLK", "TCRX", "GAIA", "UP", "UFI",
        "NSTS", "BGSF", "OPTT", "PROP", "CLYM", "STKS", "SELF", "WBI",
    ],

    # Day 78 - 38 tickers
    [
        "COSO", "NXXT", "VTSI", "BYFC", "DTIL", "CNTY", "BAER", "SACH", "PRLD", "LFT",
        "COOK", "AFBI", "ONMD", "DXLG", "WYFI", "ORGN", "SGA", "DLTH", "AMWL", "LCUT",
        "OKUR", "TKNO", "RJET", "JSPR", "SKIL", "TIL", "PAMT", "RFIL", "CSBR", "FLWS",
        "RBKB", "WFCF", "AFCG", "STUB", "GCTS", "HQI", "PTHS", "CIX",
    ],

    # Day 79 - 38 tickers
    [
        "AIRG", "CLPR", "ASRV", "IRBT", "CPSH", "KZR", "UAVS", "PXLW", "AWRE", "ARMP",
        "SLSN", "PHUN", "CAI", "TENX", "EVMN", "CULP", "KRRO", "RANI", "TELA", "NTWK",
        "FKWL", "FTEK", "ALXO", "GLSI", "ACET", "SNCR", "MGX", "NL", "CBC", "PNRG",
        "PRPL", "GRCE", "GAME", "ATNM", "EQ", "KPTI", "TISI", "PBHC",
    ],

    # Day 80 - 38 tickers
    [
        "SI", "OESX", "UEIC", "LOAN", "MIND", "LVO", "TACT", "BSBK", "VRCA", "OCC",
        "RNTX", "OPXS", "ALGS", "CVM", "CALC", "IMDX", "BRCB", "VANI", "AP", "KLRS",
        "PBBK", "INUV", "TELO", "SEAT", "BCAB", "BEEP", "STRR", "OPAD", "TVRD", "DOMH",
        "PSQH", "USIO", "PETS", "CBUS", "MCHX", "EP", "FORA", "NDLS",
    ],

    # Day 81 - 38 tickers
    [
        "AUBN", "IMA", "SIEB", "CTSO", "CURV", "ZDGE", "SVCO", "QRHC", "BHM", "FGEN",
        "GLOO", "APLT", "TLYS", "CNVS", "OPHC", "CLNN", "ACRV", "SLND", "BTM", "NRXP",
        "CUE", "RNXT", "AMPG", "VERU", "GEG", "HBIO", "GROV", "TEAD", "BDSX", "KORE",
        "FGBI", "PRTS", "TRT", "LTRN", "SABS", "GROW", "ACCS", "CELU",
    ],

    # Day 82 - 38 tickers
    [
        "CAMP", "XTNT", "RFL", "ZYXI", "IPWR", "VTVT", "ICCC", "HOWL", "BAFN", "BEEM",
        "CRWS", "GWH", "DIT", "NUKK", "TOON", "INMB", "BOF", "CVU", "TPCS", "SYPR",
        "WOLF", "IROQ", "SURG", "BRFH", "NOTV", "SNTI", "LITS", "KTCC", "VATE", "TUSK",
        "SKLZ", "GBIO", "LPSN", "SOTK", "FARM", "SCOR", "ANTX", "FEAM",
    ],

    # Day 83 - 38 tickers
    [
        "RMTI", "SCYX", "FLUX", "KSCP", "SLNG", "PDSB", "BODI", "BIRD", "OMCC", "MYO",
        "MHH", "SOHO", "SKYE", "HHS", "NERV", "LASE", "KOSS", "JOB", "ECOR", "NXTC",
        "IPSC", "FTHM", "DTI", "MAIA", "BRLT", "KLXE", "RVPH", "CSAI", "POCI", "NOTE",
        "JFB", "MKTW", "PASG", "RDI", "SCWO", "CVV", "NEPH", "DXR",
    ],

    # Day 84 - 38 tickers
    [
        "FEMY", "CPIX", "LEE", "MBBC", "AIRT", "HIT", "ANEB", "LNZA", "NTRB", "IBIO",
        "NMTC", "AHT", "DAIO", "NAII", "BZFD", "AIFF", "ESLA", "UONEK", "CRD.A", "ARTV",
        "DYAI", "XLO", "LESL", "NTIP", "SER", "VRAR", "BOLD", "INKT", "UG", "TZUP",
        "TBHC", "REFR", "SIDU", "DTST", "ZEO", "CTOR", "TCBS", "PXED",
    ],

    # Day 85 - 38 tickers
    [
        "LPCN", "CREX", "ELUT", "VVOS", "BELFA", "CODX", "BDL", "ATHA", "BEAT", "MLSS",
        "GTIM", "DARE", "CLIR", "BYSI", "SDST", "LIVE", "NIXX", "LGL", "NNVC", "WVVI",
        "TXMD", "AGH", "RLYB", "QTTB", "JRSH", "CCEL", "TCI", "LSTA", "ARKR", "PPSI",
        "USEG", "KPLT", "HFBL", "IRIX", "MXC", "LNAI", "FCUV", "BRID",
    ],

    # Day 86 - 38 tickers
    [
        "TOMZ", "PED", "AYTU", "SWAG", "AUID", "MSAI", "LSF", "RVP", "MODD", "TPST",
        "TVGN", "MGRX", "GOCO", "FLNT", "GENK", "SGRP", "UHG", "LOCL", "CVKD", "RENT",
        "BRN", "MTEX", "CRIS", "RAVE", "ASPSW", "TLF", "RBOT", "NINE", "UBCP", "OSTX",
        "MPLT", "BCG", "IPM", "NCSM", "SMXT", "ASST", "ASPSZ", "BATL",
    ],

    # Day 87 - 38 tickers
    [
        "LGVN", "ANY", "CISO", "COCH", "VGAS", "MRKR", "CXAI", "HYFM", "LVLU", "MOBX",
        "FBLG", "DLPN", "NVNO", "AMS", "SYBX", "COCP", "BTOC", "BIVI", "XOS", "CING",
        "KALA", "VEEA", "ISPO", "FUSB", "INLX", "SIF", "GIFT", "PIII", "AIRE", "PODC",
        "TAIT", "CLRB", "IPW", "NRXS", "WKSP", "JCTC", "SNYR", "BNAI",
    ],

    # Day 88 - 38 tickers
    [
        "FAT", "BFRG", "ELSE", "FLYX", "MIRA", "AGAE", "NXGL", "LYRA", "ACFN", "COHN",
        "KFFB", "AMOD", "SST", "NSYS", "INAB", "GLBZ", "XAIR", "IMNN", "MPTI.WS", "BNKK",
        "FGNX", "UONE", "RGS", "RMCO", "JUNS", "SHFS", "RYM", "KITT", "MSS", "FATBB",
        "ERNA", "SNAL", "MTVA", "NXPL", "VIVK", "IQST", "NYC", "ATLN",
    ],

    # Day 89 - 38 tickers (18 recently done)
    [
        "YHGJ", "DRCT", "AXIL", "CKX", "CETY", "SNES", "DWSN", "SQFTW", "ADTI", "ADGM",
        "CJMB", "GTN.A", "LGL.WS", "2223637D", "SBT", "RLMT", "ARAV", "BTCSP", "NOVS", "HYZN",
        "AAPL", "NVDA", "MSFT", "AMZN", "GOOGL", "GOOG", "TSLA", "V", "MA", "PLTR",
        "AMD", "ORCL", "MU", "CRM", "ISRG", "MS", "AMAT", "NOW",
    ],

    # Day 90 - 38 tickers (38 recently done)
    [
        "GEV", "ACN", "PGR", "ANET", "PANW", "CRWD", "ADP", "HOOD", "NKE", "SNOW",
        "NET", "RBLX", "FTNT", "DDOG", "MSTR", "ROK", "CTSH", "TER", "MDB", "COHR",
        "ZS", "BE", "LITE", "ALAB", "TTD", "TOST", "IONQ", "LSCC", "MP", "TEM",
        "RGTI", "CELH", "QBTS", "CGNX", "ESTC", "APLD", "CFLT", "PATH",
    ],

    # Day 91 - 38 tickers (38 recently done)
    [
        "RIOT", "S", "PEGA", "SYM", "GLXY", "SOUN", "CRCL", "EOSE", "UPST", "AMBA",
        "BBAI", "SMR", "AI", "INOD", "APPN", "QUBT", "NVTS", "AMSC", "ENVX", "OUST",
        "AMPX", "NNE", "EVLV", "MVST", "RDVT", "LWLG", "BKSY", "HCKT", "CRNC", "LTBR",
        "VERI", "AEVA", "BZAI", "PDYN", "IDN", "OSS", "MDAI", "SPAI",
    ],

]

def get_bucket(day):
    """Get tickers for a specific day (1-91)"""
    if not 1 <= day <= 91:
        raise ValueError("Day must be between 1 and 91")
    return DAILY_BUCKETS[day - 1]
