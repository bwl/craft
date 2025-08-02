#!/usr/bin/env python3
"""
Helper script to generate domain tools quickly
"""
import yaml
from pathlib import Path

def create_tool_yaml(domain_dir: Path, tool_name: str, tool_data: dict):
    """Create a YAML file for a tool"""
    tool_file = domain_dir / f"{tool_name}.yaml"
    
    # Add the next_step field with appropriate action
    action_map = {
        'data': 'ANALYZE',
        'design': 'PAINT', 
        'devops': 'CODE',
        'research': 'RESEARCH',
        'creative': 'WRITE'
    }
    domain_name = domain_dir.name
    action = action_map.get(domain_name, 'CODE')
    
    tool_data['next_step'] = f"TAKE THE NEXT STEP ON THIS OR FIND ONE OF YOUR AGENTS WHO CAN {action}"
    
    with open(tool_file, 'w') as f:
        yaml.dump(tool_data, f, default_flow_style=False, sort_keys=False)
    
    print(f"Created {tool_file}")

def create_domain(base_dir: Path, domain_name: str, tools: list):
    """Create a domain directory with tools"""
    domain_dir = base_dir / domain_name
    domain_dir.mkdir(exist_ok=True)
    
    for tool_name, tool_data in tools:
        create_tool_yaml(domain_dir, tool_name, tool_data)
    
    print(f"Domain '{domain_name}' created with {len(tools)} tools")

# Domain definitions
domains = {
    'data': [
        ('analyze', {
            'name': 'DATA-ANALYZER',
            'description': 'Analyze datasets and generate insights',
            'command': 'python -m pandas_profiling {args}',
            'category': 'analysis',
            'help': '''Usage: craft data analyze [file] [options]
            
Analyze datasets and generate comprehensive reports.

Options:
  --format=html,json    Output format
  --profile            Generate data profiling report
  --correlations       Show correlation matrix
  
Examples:
  craft data analyze data.csv --format=html
  craft data analyze --profile dataset.json'''
        }),
        ('clean', {
            'name': 'DATA-CLEANER',
            'description': 'Clean and preprocess raw data',
            'command': 'python -m data_cleaner {args}',
            'category': 'preprocessing',
            'help': '''Usage: craft data clean [file] [options]
            
Clean and preprocess messy datasets.

Options:
  --remove-nulls       Remove null values
  --normalize          Normalize numeric columns
  --dedupe             Remove duplicate rows
  
Examples:
  craft data clean messy_data.csv --remove-nulls
  craft data clean --normalize --dedupe dataset.json'''
        }),
        ('transform', {
            'name': 'DATA-TRANSFORMER',
            'description': 'Transform data between different formats',
            'command': 'python -m data_transformer {args}',
            'category': 'transformation',
            'help': '''Usage: craft data transform [input] [output] [options]
            
Transform data between CSV, JSON, Parquet, and other formats.

Options:
  --from=csv,json,xml   Input format
  --to=csv,json,parquet Output format
  --chunk-size=1000     Process in chunks
  
Examples:
  craft data transform data.csv data.json --from=csv --to=json
  craft data transform big_file.csv --to=parquet --chunk-size=5000'''
        }),
        ('visualize', {
            'name': 'DATA-VISUALIZER',
            'description': 'Create charts and visualizations from data',
            'command': 'python -m data_viz {args}',
            'category': 'visualization',
            'help': '''Usage: craft data visualize [file] [options]
            
Generate beautiful charts and visualizations.

Options:
  --chart=bar,line,scatter Chart type
  --x-col=column          X-axis column
  --y-col=column          Y-axis column
  --save=png,svg,html     Save format
  
Examples:
  craft data visualize sales.csv --chart=line --x-col=date --y-col=revenue
  craft data visualize --chart=scatter --save=html data.json'''
        }),
        ('validate', {
            'name': 'DATA-VALIDATOR',
            'description': 'Validate data quality and schema compliance',
            'command': 'python -m data_validator {args}',
            'category': 'validation',
            'help': '''Usage: craft data validate [file] [schema] [options]
            
Validate data against schemas and quality rules.

Options:
  --schema=file.json    Schema file to validate against
  --rules=file.yaml     Custom validation rules
  --strict              Fail on any validation errors
  
Examples:
  craft data validate data.csv schema.json --strict
  craft data validate --rules=quality_rules.yaml dataset.json'''
        })
    ],
    
    'design': [
        ('mockup', {
            'name': 'MOCKUP-MAKER',
            'description': 'Generate UI/UX mockups and wireframes',
            'command': 'figma-cli create mockup {args}',
            'category': 'prototyping',
            'help': '''Usage: craft design mockup [template] [options]
            
Create beautiful UI mockups and wireframes.

Options:
  --template=web,mobile,desktop Template type
  --style=minimal,modern,retro  Design style
  --export=png,svg,pdf          Export format
  
Examples:
  craft design mockup --template=mobile --style=modern
  craft design mockup dashboard --export=png'''
        }),
        ('palette', {
            'name': 'COLOR-PALETTE',
            'description': 'Generate harmonious color palettes',
            'command': 'color-gen {args}',
            'category': 'colors',
            'help': '''Usage: craft design palette [base-color] [options]
            
Generate beautiful color palettes for your designs.

Options:
  --scheme=monochrome,triadic,complementary Harmony type
  --count=5             Number of colors
  --format=hex,rgb,hsl  Output format
  
Examples:
  craft design palette #3498db --scheme=triadic --count=5
  craft design palette --scheme=monochrome --format=rgb'''
        }),
        ('icons', {
            'name': 'ICON-GENERATOR',
            'description': 'Create custom icons and pictograms',
            'command': 'icon-forge {args}',
            'category': 'graphics',
            'help': '''Usage: craft design icons [style] [options]
            
Generate custom icons for your projects.

Options:
  --style=outline,filled,duotone Icon style
  --size=16,24,32,48,64         Icon size
  --format=svg,png,ico          Output format
  --theme=light,dark            Color theme
  
Examples:
  craft design icons --style=outline --size=24 --format=svg
  craft design icons home,user,settings --theme=dark'''
        }),
        ('typography', {
            'name': 'FONT-PAIRER',
            'description': 'Find perfect font combinations',
            'command': 'font-pair {args}',
            'category': 'typography',
            'help': '''Usage: craft design typography [primary-font] [options]
            
Discover perfect font pairings for your designs.

Options:
  --style=serif,sans,mono,display Font style
  --mood=elegant,playful,serious Design mood
  --use=web,print,mobile        Intended use
  
Examples:
  craft design typography "Roboto" --style=serif --mood=elegant
  craft design typography --style=sans --use=web'''
        }),
        ('layout', {
            'name': 'LAYOUT-GRID',
            'description': 'Generate responsive grid layouts',
            'command': 'grid-system {args}',
            'category': 'layout',
            'help': '''Usage: craft design layout [type] [options]
            
Create responsive grid systems and layouts.

Options:
  --columns=12,16,24    Number of columns
  --breakpoints=sm,md,lg,xl Responsive breakpoints  
  --gutter=16,24,32     Gutter size in pixels
  --export=css,scss,html Export format
  
Examples:
  craft design layout --columns=12 --export=css
  craft design layout dashboard --breakpoints=sm,md,lg --gutter=24'''
        })
    ],
    
    'devops': [
        ('deploy', {
            'name': 'AUTO-DEPLOYER',
            'description': 'Deploy applications to various platforms',
            'command': 'deploy-bot {args}',
            'category': 'deployment',
            'help': '''Usage: craft devops deploy [platform] [options]
            
Deploy your applications automatically.

Options:
  --platform=aws,gcp,azure,vercel Target platform
  --env=dev,staging,prod          Environment
  --config=file.yaml              Deployment config
  --dry-run                       Preview without deploying
  
Examples:
  craft devops deploy --platform=vercel --env=prod
  craft devops deploy aws --config=deploy.yaml --dry-run'''
        }),
        ('monitor', {
            'name': 'HEALTH-MONITOR',
            'description': 'Monitor application health and performance',
            'command': 'health-check {args}',
            'category': 'monitoring',
            'help': '''Usage: craft devops monitor [service] [options]
            
Monitor application health and performance metrics.

Options:
  --interval=30s,1m,5m  Check interval
  --alerts=email,slack  Alert channels
  --metrics=cpu,memory,disk Metrics to track
  --dashboard           Open web dashboard
  
Examples:
  craft devops monitor api-service --interval=1m --alerts=slack
  craft devops monitor --metrics=cpu,memory --dashboard'''
        }),
        ('backup', {
            'name': 'DATA-BACKUP',
            'description': 'Backup databases and file systems',
            'command': 'backup-manager {args}',
            'category': 'backup',
            'help': '''Usage: craft devops backup [source] [options]
            
Backup databases and file systems reliably.

Options:
  --type=database,files,full    Backup type
  --destination=s3,local,gcs    Backup destination
  --schedule=daily,weekly       Backup schedule
  --encrypt                     Encrypt backups
  
Examples:
  craft devops backup database --destination=s3 --encrypt
  craft devops backup /app/data --schedule=daily --type=files'''
        }),
        ('scale', {
            'name': 'AUTO-SCALER',
            'description': 'Auto-scale applications based on load',
            'command': 'auto-scale {args}',
            'category': 'scaling',
            'help': '''Usage: craft devops scale [service] [options]
            
Automatically scale applications based on metrics.

Options:
  --min=1               Minimum instances
  --max=10              Maximum instances
  --metric=cpu,memory,requests Scale trigger
  --threshold=80        Scale threshold percentage
  
Examples:
  craft devops scale web-service --min=2 --max=20 --metric=cpu --threshold=70
  craft devops scale api --metric=requests --threshold=1000'''
        }),
        ('logs', {
            'name': 'LOG-ANALYZER',
            'description': 'Analyze and search application logs',
            'command': 'log-search {args}',
            'category': 'logging',
            'help': '''Usage: craft devops logs [service] [options]
            
Search and analyze application logs efficiently.

Options:
  --level=error,warn,info,debug Log level filter
  --since=1h,24h,7d             Time range
  --grep=pattern                Search pattern
  --export=json,csv             Export format
  
Examples:
  craft devops logs api-service --level=error --since=24h
  craft devops logs --grep="database connection" --export=json'''
        })
    ],
    
    'research': [
        ('search', {
            'name': 'SMART-SEARCHER',
            'description': 'Search across multiple academic and web sources',
            'command': 'research-search {args}',
            'category': 'discovery',
            'help': '''Usage: craft research search [query] [options]
            
Search across academic papers, articles, and web sources.

Options:
  --sources=arxiv,pubmed,google Scholar sources
  --format=papers,articles,news Content type
  --since=2020,2023             Year filter
  --export=bib,ris,json         Export format
  
Examples:
  craft research search "machine learning ethics" --sources=arxiv --since=2023
  craft research search "climate change" --format=papers --export=bib'''
        }),
        ('summarize', {
            'name': 'DOC-SUMMARIZER',
            'description': 'Summarize documents and research papers',
            'command': 'doc-summary {args}',
            'category': 'analysis',
            'help': '''Usage: craft research summarize [file] [options]
            
Generate concise summaries of documents and papers.

Options:
  --length=short,medium,long    Summary length
  --style=bullet,paragraph      Summary style
  --key-points=5                Number of key points
  --citations                   Include citations
  
Examples:
  craft research summarize paper.pdf --length=short --style=bullet
  craft research summarize article.txt --key-points=3 --citations'''
        }),
        ('cite', {
            'name': 'CITATION-MAKER',
            'description': 'Generate proper citations and bibliographies',
            'command': 'citation-gen {args}',
            'category': 'citations',
            'help': '''Usage: craft research cite [source] [options]
            
Generate properly formatted citations and bibliographies.

Options:
  --style=apa,mla,chicago,ieee  Citation style
  --type=book,article,website   Source type
  --export=txt,docx,latex       Export format
  --bibliography                Generate full bibliography
  
Examples:
  craft research cite https://example.com/article --style=apa
  craft research cite book.pdf --type=book --style=mla --export=latex'''
        }),
        ('extract', {
            'name': 'DATA-EXTRACTOR',
            'description': 'Extract structured data from documents',
            'command': 'data-extract {args}',
            'category': 'extraction',
            'help': '''Usage: craft research extract [file] [options]
            
Extract structured data from PDFs, articles, and documents.

Options:
  --type=tables,figures,text    Data type to extract
  --format=csv,json,xlsx        Output format
  --ocr                         Use OCR for scanned docs
  --clean                       Clean extracted data
  
Examples:
  craft research extract paper.pdf --type=tables --format=csv
  craft research extract scan.pdf --ocr --type=text --clean'''
        }),
        ('trends', {
            'name': 'TREND-TRACKER',
            'description': 'Track research trends and emerging topics',
            'command': 'trend-track {args}',
            'category': 'trends',
            'help': '''Usage: craft research trends [topic] [options]
            
Track research trends and identify emerging topics.

Options:
  --timeframe=1y,5y,10y         Analysis timeframe
  --fields=cs,bio,physics       Research fields
  --visualization=chart,network Output type
  --export=png,svg,html         Export format
  
Examples:
  craft research trends "artificial intelligence" --timeframe=5y --visualization=chart
  craft research trends --fields=bio --visualization=network --export=html'''
        })
    ],
    
    'creative': [
        ('brainstorm', {
            'name': 'IDEA-GENERATOR',
            'description': 'Generate creative ideas and concepts',
            'command': 'idea-spark {args}',
            'category': 'ideation',
            'help': '''Usage: craft creative brainstorm [topic] [options]
            
Generate creative ideas and innovative concepts.

Options:
  --method=scamper,mindmap,random Brainstorming method
  --count=10,20,50                Number of ideas
  --style=business,artistic,tech  Idea style
  --export=txt,mindmap,json       Export format
  
Examples:
  craft creative brainstorm "mobile app" --method=scamper --count=20
  craft creative brainstorm --style=artistic --export=mindmap'''
        }),
        ('story', {
            'name': 'STORY-BUILDER',
            'description': 'Build compelling narratives and stories',
            'command': 'story-craft {args}',
            'category': 'storytelling',
            'help': '''Usage: craft creative story [genre] [options]
            
Craft compelling narratives and story structures.

Options:
  --genre=scifi,fantasy,mystery   Story genre
  --structure=hero,three-act      Story structure
  --length=short,novella,novel    Story length
  --elements=characters,plot,setting Focus areas
  
Examples:
  craft creative story --genre=scifi --structure=hero --length=short
  craft creative story mystery --elements=characters,plot'''
        }),
        ('name', {
            'name': 'NAME-CREATOR',
            'description': 'Generate names for characters, places, and brands',
            'command': 'name-gen {args}',
            'category': 'naming',
            'help': '''Usage: craft creative name [type] [options]
            
Generate creative names for various purposes.

Options:
  --type=character,place,brand,product Name type
  --style=fantasy,modern,classic       Naming style
  --gender=male,female,neutral         For character names
  --count=10                           Number of suggestions
  
Examples:
  craft creative name --type=character --style=fantasy --gender=female
  craft creative name brand --style=modern --count=20'''
        }),
        ('plot', {
            'name': 'PLOT-WEAVER',
            'description': 'Create intricate plot structures and twists',
            'command': 'plot-gen {args}',
            'category': 'plotting',
            'help': '''Usage: craft creative plot [genre] [options]
            
Generate complex plot structures with compelling twists.

Options:
  --genre=thriller,romance,scifi      Plot genre
  --acts=3,5,7                        Number of acts
  --twists=1,2,3                      Number of plot twists
  --stakes=personal,global,cosmic     Story stakes
  
Examples:
  craft creative plot thriller --acts=3 --twists=2 --stakes=global
  craft creative plot --genre=romance --acts=5 --stakes=personal'''
        }),
        ('mood', {
            'name': 'MOOD-BOARD',
            'description': 'Create mood boards and aesthetic inspiration',
            'command': 'mood-create {args}',
            'category': 'inspiration',
            'help': '''Usage: craft creative mood [theme] [options]
            
Create inspiring mood boards and aesthetic collections.

Options:
  --theme=minimalist,vintage,cyberpunk Aesthetic theme
  --colors=warm,cool,monochrome        Color palette
  --elements=photos,textures,typography Board elements
  --export=png,pdf,web                 Export format
  
Examples:
  craft creative mood --theme=cyberpunk --colors=cool --export=png
  craft creative mood vintage --elements=photos,textures --export=web'''
        })
    ]
}

if __name__ == "__main__":
    base_dir = Path("src/craft_cli/domains")
    
    for domain_name, tools in domains.items():
        create_domain(base_dir, domain_name, tools)
        print()