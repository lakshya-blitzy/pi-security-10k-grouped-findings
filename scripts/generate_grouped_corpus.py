from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "security_fixtures"
PATTERNS = [
    'query_{i} = "SELECT * FROM users WHERE id = " + user_input_{i}',
    'subprocess.run("convert " + path_{i}, shell=True)',
    'hashlib.md5(secret_{i}.encode()).hexdigest()',
    'random.randint(0, 999999)',
    'pickle.loads(payload_{i})',
    'yaml.load(data_{i}, Loader=yaml.Loader)',
    'open("/tmp/" + filename_{i}, "w")',
    'requests.get(url_{i}, verify=False)',
    'assert supplied_{i} == expected_{i}',
    'password_{i} = "Hardcoded_Test_Password_{i}"',
]

def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    for old in ROOT.glob("fixture_*.py"):
        old.unlink()

    for file_idx in range(1000):
        lines = [
            '"""Static security-analysis fixture. Do not execute or deploy."""'
        ]
        for pattern_idx, pattern in enumerate(PATTERNS):
            i = file_idx * len(PATTERNS) + pattern_idx
            lines.append(f"def fixture_{i}():")
            lines.append(f"    {pattern.format(i=i)}")
            lines.append("    return None")
            lines.append("")
        (ROOT / f"fixture_{file_idx:04d}.py").write_text(
            "\n".join(lines)
        )

    print("Generated 1,000 files with 10,000 candidate instances.")

if __name__ == "__main__":
    main()
