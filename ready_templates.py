import sys
import os


HTML_TEMPLATE_FN = "html_template.html"
README_TEMPLATE_FN = "readme_template.md"

GITHUB_ID="kh-kim"
REPO_NAME="arxiv-translator"


def main(en_mmd_fn):
    en_mmd_lines = []
    with open(en_mmd_fn, "r") as f:
        for line in f:
            en_mmd_lines.append(line.replace("\n", ""))

    ko_mmd_fn = en_mmd_fn.replace(".mmd", ".ko.mmd")
    ko_mmd_lines = []
    with open(ko_mmd_fn, "r") as f:
        for line in f:
            ko_mmd_lines.append(line.replace("\n", ""))

    arxiv_id = en_mmd_fn.split("/")[-1].split("_")[0]

    html_lines = []
    with open(HTML_TEMPLATE_FN, "r") as f:
        for line in f:
            html_lines.append(line.replace("\n", ""))

    readme_lines = []
    with open(README_TEMPLATE_FN, "r") as f:
        for line in f:
            readme_lines.append(line.replace("\n", ""))

    def wrap(line):
        return "      '" + line.replace("\\", "\\\\").replace("'", "\\'") + "\\n' +"

    en_result_html_lines = html_lines[:6] + [wrap(line) for line in en_mmd_lines] + html_lines[6:]
    en_result_html = "\n".join(en_result_html_lines)

    with open(os.path.join(arxiv_id, "paper.en.html"), "w") as f:
        f.write(en_result_html)

    ko_result_html_lines = html_lines[:6] + [wrap(line) for line in ko_mmd_lines] + html_lines[6:]
    ko_result_html = "\n".join(ko_result_html_lines)

    with open(os.path.join(arxiv_id, "paper.ko.html"), "w") as f:
        f.write(ko_result_html)

    result_readme = "\n".join(readme_lines).format(
        title=".".join(en_mmd_fn.split("/")[-1].split(".")[:-1]).replace("_", " "),
        arxiv_url="https://arxiv.org/abs/{arxiv_id}".format(arxiv_id=arxiv_id),
        ar5iv_url="https://ar5iv.org/abs/{arxiv_id}".format(arxiv_id=arxiv_id),
        en_html_url="https://raw.githack.com/{github_id}/{repo_name}/master/{arxiv_id}/paper.en.html".format(
            github_id=GITHUB_ID,
            repo_name=REPO_NAME,
            arxiv_id=arxiv_id,
        ),
        ko_html_url="https://raw.githack.com/{github_id}/{repo_name}/master/{arxiv_id}/paper.ko.html".format(
            github_id=GITHUB_ID,
            repo_name=REPO_NAME,
            arxiv_id=arxiv_id,
        ),
    )

    with open(os.path.join(arxiv_id, "README.md"), "w") as f:
        f.write(result_readme)


if __name__ == "__main__":
    en_mmd_fn = sys.argv[1]

    main(en_mmd_fn)
