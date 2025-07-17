import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MARKETAUX_API_TOKEN = os.getenv("MARKETAUX_API_TOKEN")
KEYWORDS = ['Sustainable finance', 'green economy', 'blue economy']
KEYWORDS2 = ["green bonds", "green economy", "blue economy", "sustainable finance", "investment trust", "traded investment trust", 
            "trust discount", "board of directors", "income paying trust", "trust dividend", "trust NAV"]



FUNDS = [
    "abrdn Global Sustainable Equity Fund",
    "abrdn UK Sustainable Equity Fund",
    "Aegon Sustainable Diversified Growth Fund",
    "Aegon Sustainable Equity Fund",
    "AEW UK Impact Fund",
    "Aquila Energy Efficiency Trust",
    "Aquila European Renewables",
    "ARC TIME Social Impact Property Fund",
    "AXA Carbon Transition Global Short Duration Bond Fund",
    "AXA Carbon Transition Sterling Buy and Maintain Credit Fund",
    "AXA Global Sustainable Managed Fund",
    "AXA People & Planet Equity Fund",
    "AXA UK Sustainable Equity Fund",
    "Baillie Gifford Positive Change Fund",
    "Baillie Gifford Sustainable Growth Fund",
    "BFM Brown to Green Materials Fund (BlackRock)",
    "Bluefield Solar Income Fund",
    "CT Responsible Global Equity Fund",
    "CT Sustainable Global Equity Income Fund",
    "CT Sustainable Opportunities Global Equity Fund",
    "CT Sustainable Universal MAP Adventurous Fund",
    "CT Sustainable Universal MAP Balanced Fund",
    "CT Sustainable Universal MAP Cautious Fund",
    "CT Sustainable Universal MAP Defensive Fund",
    "CT Sustainable Universal MAP Growth Fund",
    "CT UK Sustainable Equity Fund",
    "Downing Renewables & Infrastructure",
    "Ecofin US Renewables Infrastructure",
    "EdenTree Global Impact Bond Fund",
    "EdenTree Global Select Government Bond Fund",
    "EdenTree Global Sustainable Government Bond Fund",
    "Edentree Green Future Fund",
    "EdenTree Green Infrastructure Fund",
    "Fidelity Sustainable European Equity Fund",
    "Fidelity Sustainable Global Equity Fund",
    "Fidelity Sustainable Multi-Asset Balanced Fund",
    "Fidelity Sustainable Multi-Asset Conservative Fund",
    "Fidelity Sustainable Multi-Asset Growth Fund",
    "Fidelity Sustainable UK Equity Fund",
    "Foresight Environmental Infrastructure",
    "Foresight Solar Fund",
    "FP Foresight Global Real Infrastructure Fund",
    "FP Foresight Sustainable Future Themes Fund",
    "FP Foresight Sustainable Real Estate Securities Fund",
    "FP Foresight UK Infrastructure Income Fund",
    "FP WHEB Sustainability Impact Fund",
    "Global Impact Credit Fund",
    "Global Impact Equity Fund",
    "Gore Street Energy Storage Fund",
    "Greencoat Renewables",
    "Greencoat UK Wind",
    "Gresham House Energy Storage",
    "HydrogenOne Capital Growth",
    "Impax Environmental Markets",
    "Janus Henderson Global Sustainable Equity Fund",
    "Janus Henderson Sustainable Future Technologies Fund",
    "Janus Henderson US Sustainable Equity Fund",
    "Jupiter Ecology Fund",
    "Jupiter Responsible Income Fund",
    "Liontrust Sustainable Future Cautious Managed Fund",
    "Liontrust Sustainable Future Corporate Bond",
    "Liontrust Sustainable Future Defensive Managed Fund",
    "Liontrust Sustainable Future European Growth Fund",
    "Liontrust Sustainable Future Global Growth Fund",
    "Liontrust Sustainable Future Managed Fund",
    "Liontrust Sustainable Future Managed Growth Fund",
    "Liontrust Sustainable Future Monthly Income Bond Fund",
    "Liontrust Sustainable Future UK Growth Fund",
    "Liontrust UK Ethical Fund",
    "M&G European Sustain Paris Aligned Fund",
    "M&G Global Sustain Paris Aligned Fund",
    "M&G Positive Impact Fund",
    "M&G UK Sustain Paris Aligned Fund",
    "NextEnergy Solar Fund",
    "Ninety One Funds Series III - Global Environment Fund",
    "Ninety One Funds Series III - Global Equity",
    "Ninety One Funds Series iii - Global Sustainable Equity Fund",
    "NS&I Green Savings Bonds",
    "Octopus Renewables Infrastructure Trust",
    "Premier Miton Emerging Markets Sustainable Fund",
    "Premier Miton Global Sustainable Growth Fund",
    "Premier Miton Global Sustainable Optimum Income Fund",
    "Rathbone Greenbank Defensive Return",
    "Rathbone Greenbank Global Sustainability Fund",
    "Rathbone Greenbank Global Sustainable Bond Fund",
    "Rathbone Greenbank Strategic Growth",
    "Rathbone Greenbank Total Return",
    "Rathebone Greenbank Dynamic Growth",
    "Regnan Global Equity Impact Solutions Fund",
    "Regnan Sustainable Water and Waste",
    "Renewables Infrastructure Group",
    "Schroder BSC Social Impact Trust",
    "Schroder European Climate Transition Fund",
    "Schroder Global Alternative Energy Fund",
    "Schroder Global Cities Real Estate Fund",
    "Schroder Global Sustainable Food and Water Fund",
    "Schroder Global Sustainable Growth Fund",
    "Schroder Global Sustainable Value Equity Fund",
    "Schroder Sustainable Bond Fund",
    "Schroder Sustainable Future Multi-Asset Fund",
    "Schroder Sustainable Multi-Factor Equity Fund",
    "Schroder Sustainable UK Equity Fund",
    "Schroder SUTL Cazenove Sustainable Growth Fund",
    "Schroders Capital Real Estate Impact Fund (SCREIF)",
    "SDCL Efficiency Income",
    "SJP Sustainable & Responsible Equity Fund",
    "Standard Life Future Advantage (1-5) Pension range",
    "SUTL Cazenove Charity Sustainable Multi-Asset Fund",
    "SUTL Cazenove Sustainable Balanced Fund",
    "SUTL Cazenove Sustainable Balanced Fund (Schroders)",
    "SUTL Cazenove Sustainable Growth Fund",
    "SVS AllianceBernstein Sustainable Global Equity Fund",
    "SVS AllianceBernstein Sustainable US Equity Fund",
    "T. Rowe Price Global Impact Credit Fund",
    "T. Rowe Price Global Impact Equity Fund",
    "TrinityBridge Sustainable Balanced Portfolio Fund",
    "US Solar Fund",
    "VH Global Energy Infrastructure",
    "WS Guinness Sustainable Energy Fund",
    "WS Montanaro Better World Fund"
]





RELEVANT_KEYWORDS = [
    # Core Themes
    'sustainable finance', 'green economy', 'blue economy', 'responsible investment',
    'ESG', 'SDR-labelled funds', 'impact investing', 'climate finance',
    
    # Investment & Capital Raising
    'capital raising', 'investor targeting', 'institutional investors', 'investment funds',
    'IPOs', 'secondary offerings', 'bookbuilding', 'test marketing',
    'private wealth', 'multi-asset', 'pension funds', 'fundraising',

    # Risk & Regulation
    'greenwashing', 'regulatory change', 'market intelligence', 'financial regulation',
    'non-financial risks', 'ESG metrics', 'FCA', 'investment risks',
    
    # Partnerships & Strategy
    'stakeholder engagement', 'strategic marketing', 'policy advocacy',
    'corporate broking', 'advisor integrity', 'distribution strategy',
    
    # Innovation & Research
    'SAFL Innovation and Origination Lab', 'academic collaboration', 'science-led engagement',
    
    # Environment & Climate
    'climate crisis', 'biodiversity', 'natural catastrophe', 'planetary boundaries',
    'conservation', 'net-zero', 'climate adaptation', 'renewable energy',
    'EV transition', 'tidal stream', 'sustainability solutions',
    
    # Sector Specific
    'listed solar fund', 'infrastructure investment', 'environmental finance',
    'transition economy', 'energy transition', 'sustainable business models',
    
    # Additional Triggers
    'liquidity risk', 'investment trust', 'engagement strategy', 'market sentiment',
    'discount narrowing', 'share buybacks', 'mean-reversion arbitrage',
    'institutional engagement', 'credible outputs', 'content for investors'
]

GEMINI_MODEL = "models/gemini-2.0-flash"
ARTICLE_LOOKBACK_DAYS = 3

