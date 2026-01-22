"""Configuration dataclass for the Innovation Scorer application."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, List, Dict
import json


def default_allowed_companies() -> list[str]:
    """Return the default list of allowed companies."""
    return [
        "3M", "ABB", "Adidas", "Adobe", "Airbnb", "Airbus", "Alfa Laval", "Amazon", "Apple",
        "Audi", "BASF", "Beiersdorf", "Bentley Motors", "BMW", "Boeing", "Bosch", "BSH Group",
        "Campbell Foods", "Carlsberg", "Clariant", "Coca-Cola", "Colgate Palmolive",
        "Continental", "Covestro", "Daimler", "Daimler Truck", "Danone",
        "Deutsche Telekom", "Dow", "Dow Chemical Company", "DSM", "DSM Firmenich", "DuPont",
        "Eastman Chemical", "Electrolux", "Enel", "Engie", "Ericsson", "Evonik",
        "Facebook/Meta", "Ferrari", "Fiat Chrysler Automobiles/Stellantis", "Ford",
        "Forvia", "GE", "GE Aerospace", "GE Healthcare", "GE Power", "GE Renewable Energy",
        "General Motors", "Goodyear", "Google", "Groupe PSA/Stellantis", "Haier",
        "Heineken", "Henkel", "HP", "Huawei", "Ikea", "Jacobs Douwe Egberts",
        "Jaguar Land Rover", "Johnson & Johnson", "Kellanova", "Kimberly Clark",
        "KION Group", "Knorr Bremse", "Kraft Heinz", "L'Oreal", "Lego", "Lenovo",
        "LG Electronics", "Logitech", "Lyft", "Maersk", "Mann Hummel", "Mars",
        "McLaren Automotive", "Mercedes Benz", "Meta", "Michelin", "Microsoft", "Miele",
        "Mondelez", "NASA", "Nestle", "Netflix", "Nike", "Nissan", "Nokia", "Novo Nordisk",
        "PepsiCo", "Philips", "Porsche", "Procter & Gamble", "Reckitt", "Renault",
        "Rolls-Royce", "Samsung", "Scania", "Schaeffler", "Schneider Electric", "Siemens",
        "Siemens Healthineers", "Signify", "Spotify", "Starbucks", "Stora Enso", "Sulzer",
        "Tesla", "Tetra Pak", "Thales", "Thales Alenia Space", "Toyota", "Twitter",
        "Twitter / X", "Uber", "Unilever", "Volkswagen", "Volvo Cars", "Volvo Group",
        "W.L. Gore", "Walmart", "Walt Disney", "Whirlpool", "Zalando",
        "AB InBev", "ABN AMRO", "Accor", "Air France-KLM", "Air Liquide", "AkzoNobel",
        "Alibaba", "Allianz", "Alstom", "Amcor", "American Express", "Arla Foods", "Asics",
        "AstraZeneca", "Avery Dennison", "AXA", "Baker Hughes", "Barclays", "Barilla",
        "Barry Callebaut", "Bayer", "BNP Paribas", "Boehringer Ingelheim", "Booking.com",
        "Borealis", "BP", "Bupa", "Canon", "Cargill", "Carl Zeiss", "Carrier", "Chanel",
        "Cisco", "Citi", "Cognizant", "Coty", "Danfoss", "DB Schenker", "Dell", "Dematic",
        "Deutsche Bahn", "Deutsche Post DHL", "DHL", "Diageo", "Dyson", "E.ON", "eBay",
        "EDF", "Eni", "Equinor", "Erste Group", "Essity", "Estee Lauder", "Expedia",
        "Ferrero", "Fujitsu", "GE Vernova", "General Mills", "Grundfos", "Haleon",
        "Hewlett-Packard", "Hilti", "Hitachi", "Hitachi Energy", "Holcim", "Honeywell",
        "Hugo Boss", "Husqvarna", "IBM", "Intel", "Intuit", "Kellogg", "Kenvue", "Kone",
        "Konica Minolta", "Kuehne + Nagel", "Lamborghini", "Linde Group", "LinkedIn",
        "Lloyds Bank", "Lufthansa", "Mastercard", "Merck Group", "Mitsubishi", "Nordea",
        "Novartis", "Novozymes", "Oracle", "Orange", "Panasonic", "Pandora", "Paypal",
        "Pfizer", "Puma", "Roche", "Roche Diagnostics", "Rockwell Automation", "Sanofi",
        "SAP", "Scandinavian Airlines System SAS", "Shell",
        "Siemens Energy", "Sky", "Solvay", "Sony", "Sony Mobile", "Swarovski", "Swiss Re",
        "Telefonica", "Tencent", "Tesco", "Thermo Fisher Scientific", "Thyssenkrupp",
        "Toshiba", "TotalEnergies", "Vestas", "Virgin", "Visa", "Vodafone",
        "Zurich Insurance"
    ]


def default_company_variants() -> dict[str, list[str]]:
    """Return the default company name variants mapping."""
    return {
        "Amazon": ["Amazon Web Services", "AWS", "Amazon.com", "Amazon EU"],
        "Meta": ["Facebook", "Meta Platforms", "Facebook/Meta"],
        "Google": ["Alphabet", "Google LLC"],
        "HP": ["Hewlett Packard", "Hewlett-Packard", "HP Inc", "HPE"],
        "Coca-Cola": ["Coca Cola", "The Coca-Cola Company"],
        "Rolls-Royce": ["Rolls Royce", "Rolls-Royce plc"],
        "BMW": ["BMW Group"],
        "Mercedes Benz": ["Mercedes-Benz", "Mercedes-Benz Group"],
        "Volkswagen": ["VW", "Volkswagen Group"],
        "Twitter / X": ["Twitter", "X"],
        "DSM Firmenich": ["DSM-Firmenich", "dsm-firmenich"],
        "Deutsche Post DHL": ["Deutsche Post", "DHL Group"],
        "Procter & Gamble": ["P&G", "Procter and Gamble"],
        "Johnson & Johnson": ["J&J"],
        "L'Oreal": ["Loreal", "L'Oréal"],
        "Maersk": ["A.P. Moller - Maersk", "APM Maersk"],
        "Scandinavian Airlines System SAS": ["SAS", "Scandinavian Airlines"]
    }


def default_disqualify_title_bus() -> list[str]:
    """Return the default business title disqualification patterns."""
    return [
        r"\bsolutions?\b",
        r"\bsales\b",
        r"\bclient\b",
        r"\bmarketing\b",
        r"\bmkt\b",
        r"\badvertising\b",
        r"\bhr\b",
        r"\bhuman resources?\b",
        r"\btalent\b",
        r"\bacquisition\b",
        r"\brecruit\w*\b",
        r"\bfinance\b",
        r"\bcontrolling\b",
        r"\bprocurement\b",
        r"\bpurchasing\b",
        r"\boperations?\b",
        r"\blogistics?\b",
        r"\borganizational efficiency\b",
        r"\blegal\b",
        r"\bservices\b",
        r"\boffice\b",
        r"\bassistant\b",
        r"\be-?commerce\b"
    ]


def default_disqualify_title_tech() -> list[str]:
    """Return the default tech title disqualification patterns."""
    return [
        r"\bit\b|\binformation technology\b",
        r"\binfrastructure\b|\borchestration\b",
        r"\bsoftware\b|\bsoftware engineering\b",
        r"\bplatforms?\b|\bcompute\b",
        r"\bengineering\b",
        r"\bcto\b|\bcto office\b",
        r"\barchitecture\b|\barchitect\b",
        r"\bran\b|\bnetwork\b",
    ]


def default_themes() -> dict[str, list[str]]:
    """
    Return the default core themes (always active).
    
    NOTE: This is intentionally minimal - just core innovation focus.
    Event-specific themes are built dynamically from topic_keyword_packs
    based on the Event Topic you set.
    """
    return {
        "Core Innovation": [
            "innovation", "innovate", "innovative", "R&D", "research and development"
        ]
    }


def default_topic_keyword_packs() -> dict[str, list[str]]:
    """
    Return the default topic keyword packs.
    
    These are used to build dynamic event-angle themes based on the Event Topic.
    When your Event Topic contains a key (e.g., "sustainability"), the corresponding
    keywords are added to the "Event Angle (Dynamic)" theme.
    
    Example: Event Topic = "Circularity, Net Zero & Subscription Models"
    - Matches: "circular", "net zero", "subscription"
    - Creates dynamic theme with all those keywords
    """
    return {
        # Sustainability & Environment
        "sustainability": [
            "sustainability", "sustainable", "ESG", "environmental",
            "green", "eco-friendly", "responsible"
        ],
        "circular": [
            "circular economy", "circularity", "recycling", "waste reduction",
            "closed loop", "reuse", "refurbish", "repair", "repairability",
            "end of life", "material recovery", "upcycling"
        ],
        "net zero": [
            "net zero", "carbon neutral", "decarbonization", "carbon footprint",
            "emissions", "climate", "carbon reduction", "greenhouse gas"
        ],
        "climate": [
            "climate change", "climate action", "climate tech", "carbon",
            "emissions reduction", "environmental impact"
        ],
        
        # Business Models
        "subscription": [
            "subscription", "as-a-service", "service model", "XaaS",
            "recurring revenue", "product-as-a-service", "servitization"
        ],
        "business model": [
            "business model", "new business", "growth", "venture", "venturing",
            "incubator", "accelerator", "corporate venture", "portfolio",
            "revenue model", "monetization"
        ],
        
        # Digital & Technology
        "digital": [
            "digital transformation", "digital innovation", "digitization",
            "digitalization", "digital strategy"
        ],
        "ai": [
            "artificial intelligence", "AI", "generative AI", "GenAI", "LLM",
            "machine learning", "deep learning", "neural network"
        ],
        "data": [
            "data analytics", "big data", "data-driven", "data science",
            "analytics", "business intelligence"
        ],
        "iot": [
            "IoT", "internet of things", "connected devices", "smart devices",
            "sensors", "industrial IoT", "IIoT"
        ],
        
        # Customer & Experience
        "customer": [
            "customer centric", "customer-centric", "customer experience",
            "customer journey", "customer engagement", "customer value"
        ],
        "design": [
            "design thinking", "user experience", "UX", "service design",
            "human centered", "human-centered design"
        ],
        
        # Culture & Organization
        "culture": [
            "innovation culture", "culture change", "cultural transformation",
            "mindset", "ways of working"
        ],
        "agile": [
            "agile", "agility", "scrum", "lean", "sprint", "iterative"
        ],
        "leadership": [
            "leadership", "change management", "capability building",
            "talent development", "organizational change"
        ],
        
        # Collaboration & Ecosystems
        "startup": [
            "startup", "start-up", "entrepreneurship", "founder",
            "startup collaboration", "corporate-startup"
        ],
        "ecosystem": [
            "ecosystem", "open innovation", "partnership", "collaboration",
            "co-creation", "consortium", "alliance"
        ],
        "partner": [
            "partnership", "strategic partner", "external partner",
            "collaboration", "joint venture"
        ],
        
        # R&D & Operations
        "r&d": [
            "R&D", "research and development", "research", "development",
            "product development", "technology development"
        ],
        "manufacturing": [
            "manufacturing", "production", "factory", "industry 4.0",
            "smart manufacturing", "operational excellence"
        ],
        
        # Specific Event Angles
        "mobility": [
            "mobility", "automotive", "electric vehicle", "EV",
            "autonomous", "transportation", "fleet"
        ],
        "energy": [
            "energy", "renewable", "clean energy", "energy transition",
            "power", "grid", "battery", "storage"
        ],
        "health": [
            "healthcare", "health", "medical", "pharma", "biotech",
            "life sciences", "patient"
        ],
        "food": [
            "food", "nutrition", "agriculture", "agtech", "food tech",
            "alternative protein", "plant-based"
        ],
    }


def default_subthemes() -> list[str]:
    """Return the default subthemes."""
    return [
        "Customer Value",
        "AI for customer Value",
        "AI for customer experiences",
        "IoT",
        "AI Agents",
        "Scaling AI",
        "data-driven decisions",
        "efficiency with AI"
    ]


@dataclass
class ScoringConfig:
    """Configuration for the scoring engine."""
    
    # Event settings
    event_name: str = "External partnerships, internal ventures, startups and innovation"
    event_date: str = "April 29, 2026"
    event_location: str = "Munich"
    event_host: str = "Shell"
    event_topic_override: str = "Internal and External Startups & Ecosystems & Partnerships & Ventures"
    main_theme: str = "external partnerships, internal ventures, startups and innovation and ecosystems"
    subthemes: list[str] = field(default_factory=default_subthemes)
    
    # Scoring weights
    w_senior_top: int = 40  # VP and Director weight
    w_head: int = 25  # Head of department weight
    w_title_innov: int = 35  # Innovation in title weight
    w_text_innov: int = 20  # Innovation in text weight
    w_theme_hit: int = 3  # Points per theme hit
    w_theme_bonus: int = 6  # Bonus for 2+ hits in a theme
    max_theme_points: int = 30  # Maximum theme points
    w_title_event_hit: int = 8  # Event angle keyword in title
    max_title_event_points: int = 24  # Maximum event angle points
    
    # Penalties
    penalty_anti_function: int = -35  # Anti-function penalty
    
    # Thresholds
    min_theme_hits_total: int = 2  # Minimum theme hits required
    min_innov_signals_text: int = 2  # Minimum innovation signals in text
    
    # Output settings
    top_n: int = 200  # Number of top profiles to export
    
    # Company lists
    allowed_companies: list[str] = field(default_factory=default_allowed_companies)
    company_variants: dict[str, list[str]] = field(default_factory=default_company_variants)
    
    # Disqualification patterns
    disqualify_title_bus: list[str] = field(default_factory=default_disqualify_title_bus)
    disqualify_title_tech: list[str] = field(default_factory=default_disqualify_title_tech)
    
    # Themes and keywords
    themes: dict[str, list[str]] = field(default_factory=default_themes)
    topic_keyword_packs: dict[str, list[str]] = field(default_factory=default_topic_keyword_packs)
    
    def to_json(self) -> str:
        """Serialize the configuration to JSON."""
        return json.dumps(asdict(self), indent=2)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert the configuration to a dictionary."""
        return asdict(self)
    
    @classmethod
    def from_json(cls, json_str: str) -> "ScoringConfig":
        """Deserialize a configuration from JSON."""
        data = json.loads(json_str)
        return cls(**data)
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ScoringConfig":
        """Create a configuration from a dictionary."""
        return cls(**data)
    
    @classmethod
    def get_default(cls) -> "ScoringConfig":
        """Return a new instance with all default values."""
        return cls()


# Pre-built regex pattern lists (for reference in scoring)
VP_PATTERNS = [
    r"\bsvp\b", r"\bevp\b", r"\bavp\b", r"\bvp\b", r"\bvice president\b"
]

DIRECTOR_INNOV_PATTERNS = [
    r"\bdirector\b.*\binnovation\b",
    r"\bdirector\b.*\bopen innovation\b",
    r"\bdirector\b.*\bventure\b|\bdirector\b.*\bventuring\b",
    r"\bdirector\b.*\bR\s*&\s*D\b|\bdirector\b.*\bR&D\b",
    r"\bdirector\b.*\bforesight\b|\bdirector\b.*\bnew business\b|\bdirector\b.*\bbusiness model\b",
    r"\bdirector\b.*\bsustainab\w*\b|\bdirector\b.*\bcircular\w*\b|\bdirector\b.*\bnet zero\b",
    # NOTE: AI/Digital patterns removed - they only score via topic_keyword_packs now
]

HEAD_PATTERNS = [
    r"\bhead of\b",
    r"\bhead\b(?!quarters)\b"
]

INNOV_RD_STRONG = [
    r"\binnovation\b",
    r"\bopen innovation\b",
    r"\bventure\b|\bventuring\b|\bcorporate venture\b",
    r"\bR\s*&\s*D\b|\bR&D\b",
    r"\bresearch\s*(and|&)\s*development\b",
    r"\bresearch\b",
    r"\bnew business\b|\bbusiness model\b",
    r"\bforesight\b|\bscenario\b|\btrend\b|\bhorizon scanning\b|\bstrategic foresight\b",
    r"\bincubator\b|\baccelerator\b|\becosystem\b",
    r"\bsustainab\w*\b|\bcircular\w*\b|\bnet zero\b|\bdecarbon\w*\b|\besg\b",
    # NOTE: AI/Digital/Data patterns removed - they only score via topic_keyword_packs now
]

TITLE_INNOV_RD = [
    r"\binnovation\b",
    r"\bopen innovation\b",
    r"\bventure\b|\bventuring\b",
    r"\bR\s*&\s*D\b|\bR&D\b",
    r"\bnew business\b|\bbusiness model\b",
    r"\bforesight\b",
    r"\bincubator\b|\baccelerator\b|\becosystem\b",
    r"\bsustainab\w*\b|\bcircular\w*\b|\bnet zero\b",
    # NOTE: AI/Digital patterns removed - they only score via topic_keyword_packs now
]

ANTI_FUNCTION = [
    r"\boperations\b|\bops\b",
    r"\bsupply chain\b|\blogistics\b|\bmanufacturing\b",
    r"\bprocurement\b|\bsourcing\b",
    r"\breal estate\b|\bfacilities\b|\bworkplace\b",
    r"\bmedia\b|\bcommunications?\b|\bpr\b|\bbrand\b|\bmarketing\b",
    r"\bhr\b|\bhuman resources\b|\btalent\b",
    r"\bfinance\b|\baccounting\b|\btreasury\b",
    r"\blegal\b|\bcompliance\b|\brisk\b",
]
