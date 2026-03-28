import urllib.request
import os
import datetime

REPO_BASE = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/"
TARGET_REPO = "https://github.com/blackmatrix7/ios_rule_script"

# Retrieve creator name for AI.yaml author field. Assuming standard checkout structure.
def get_creator_name():
    if 'GITHUB_REPOSITORY' in os.environ:
        return os.environ['GITHUB_REPOSITORY'].split('/')[0]
    cwd = os.getcwd()
    return os.path.basename(os.path.dirname(cwd))

CREATOR_NAME = get_creator_name()

MAPPINGS = [
    {
        "target": "Clash/DIRECT/apple.yaml",
        "sources": ["rule/Clash/Apple/Apple_Classical.yaml"],
        "name": "Apple",
        "author": "blackmatrix7"
    },
    {
        "target": "Clash/DIRECT/China.yaml",
        "sources": ["rule/Clash/China/China_Classical.yaml"],
        "name": "China",
        "author": "blackmatrix7"
    },
    {
        "target": "Clash/DIRECT/ChinaIPs.yaml",
        "sources": ["rule/Clash/ChinaIPs/ChinaIPs_Classical.yaml"],
        "name": "ChinaIPs",
        "author": "blackmatrix7"
    },
    {
        "target": "Clash/DIRECT/Microsoft.yaml",
        "sources": ["rule/Clash/Microsoft/Microsoft.yaml"],
        "name": "Microsoft",
        "author": "blackmatrix7"
    },
    {
        "target": "Clash/PROXY/AI.yaml",
        "sources": [
            "rule/Clash/OpenAI/OpenAI.yaml",
            "rule/Clash/Gemini/Gemini.yaml",
            "rule/Clash/Claude/Claude.yaml"
        ],
        "name": "AI",
        "author": CREATOR_NAME
    },
    {
        "target": "Clash/PROXY/Google.yaml",
        "sources": ["rule/Clash/Google/Google.yaml"],
        "name": "Google",
        "author": "blackmatrix7"
    },
    {
        "target": "Clash/PROXY/Netflix.yaml",
        "sources": ["rule/Clash/Netflix/Netflix_Classical.yaml"],
        "name": "Netflix",
        "author": "blackmatrix7"
    },
    {
        "target": "Clash/PROXY/Paypal.yaml",
        "sources": ["rule/Clash/PayPal/PayPal.yaml"],
        "name": "PayPal",
        "author": "blackmatrix7"
    },
    {
        "target": "Clash/PROXY/China.yaml",
        "sources": ["rule/Clash/China/China.yaml"],
        "name": "China",
        "author": "blackmatrix7"
    }
]

def fetch_content(path):
    url = REPO_BASE + path
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    print(f"Downloading {url}...")
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def process_mapping(mapping):
    lines_set = set()
    raw_lines = []
    
    for src in mapping["sources"]:
        content = fetch_content(src)
        if not content:
            continue
        
        lines = content.splitlines()
        payload_started = False
        
        for line in lines:
            trimmed = line.strip()
            if trimmed == 'payload:':
                payload_started = True
                continue
            if payload_started and line.startswith('  - '):
                if line not in lines_set:
                    lines_set.add(line)
                    raw_lines.append(line)
                    
    domain_keyword_count = sum(1 for line in raw_lines if 'DOMAIN-KEYWORD,' in line)
    domain_suffix_count = sum(1 for line in raw_lines if 'DOMAIN-SUFFIX,' in line)
    total = len(raw_lines)
    
    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    header = f"""# NAME: {mapping['name']}
# AUTHOR: {mapping['author']}
# REPO: {TARGET_REPO}
# UPDATED: {now_str}
# DOMAIN-KEYWORD: {domain_keyword_count}
# DOMAIN-SUFFIX: {domain_suffix_count}
# TOTAL: {total}
"""
    
    final_content = header
    if total > 0:
        final_content += "payload:\n"
        raw_lines.sort()
        for line in raw_lines:
            final_content += f"{line}\n"
            
    os.makedirs(os.path.dirname(mapping["target"]), exist_ok=True)
    
    with open(mapping["target"], "w", encoding='utf-8') as f:
        f.write(final_content)
    print(f"Updated {mapping['target']} with {total} rules.")

def main():
    for mapping in MAPPINGS:
        process_mapping(mapping)

if __name__ == "__main__":
    main()
