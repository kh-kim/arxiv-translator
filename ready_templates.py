import sys
import os


PAPER_DIR = "papers"
MAIN_README_TEMPLATE_FN = "assets/main_readme_template.md"
HTML_TEMPLATE_FN = "assets/html_template.html"
README_TEMPLATE_FN = "assets/readme_template.md"

GITHUB_ID="kh-kim"
REPO_NAME="arxiv-translator"


def update_main_readme():
    main_readme_lines = []
    with open(MAIN_README_TEMPLATE_FN, "r") as f:
        for line in f:
            main_readme_lines.append(line.replace("\n", ""))

    pdf_fn_list = []
    for root, dirs, files in os.walk("."):
        for fn in files:
            if fn.endswith(".pdf") and fn[:4].isdigit() and fn[5:10].isdigit():
                pdf_fn_list.append(fn)
    pdf_fn_list.sort(reverse=True)

    arxiv_id_list = [fn[:10] for fn in pdf_fn_list]
    title_list = [fn[11:].replace(".pdf", "").replace("_", " ") for fn in pdf_fn_list]
    arxiv_url_list = [
        "https://arxiv.org/abs/{arxiv_id}".format(arxiv_id=arxiv_id)
        for arxiv_id in arxiv_id_list
    ]
    ar5iv_url_list = [
        "https://ar5iv.org/abs/{arxiv_id}".format(arxiv_id=arxiv_id)
        for arxiv_id in arxiv_id_list
    ]
    en_html_url_list = [
        "https://raw.githack.com/{github_id}/{repo_name}/master/papers/{arxiv_id}/paper.en.html".format(
            github_id=GITHUB_ID,
            repo_name=REPO_NAME,
            arxiv_id=arxiv_id,
        )
        for arxiv_id in arxiv_id_list
    ]
    ko_html_url_list = [
        "https://raw.githack.com/{github_id}/{repo_name}/master/papers/{arxiv_id}/paper.ko.html".format(
            github_id=GITHUB_ID,
            repo_name=REPO_NAME,
            arxiv_id=arxiv_id,
        )
        for arxiv_id in arxiv_id_list
    ]

    insertion_lines = [
        "| ArXiv ID | Title | ArXiv / Ar5iv | English / Korean |",
        "|:--------:|:-----:|:-------------:|:----------------:|",
    ]
    for i in range(len(pdf_fn_list)):
        insertion_lines.append(
            "| {arxiv_id} | {title} | [arXiv]({arxiv_url}){new_tab} / [ar5iv]({ar5iv_url}){new_tab} | [en]({en_html_url}){new_tab} / [ko]({ko_html_url}){new_tab} |".format(
                arxiv_id=arxiv_id_list[i],
                title=title_list[i],
                arxiv_url=arxiv_url_list[i],
                new_tab="", #"{:target=\"_blank\"}",
                ar5iv_url=ar5iv_url_list[i],
                en_html_url=en_html_url_list[i],
                ko_html_url=ko_html_url_list[i],
            )
        )

    insertion_lines = "\n".join(insertion_lines)

    result = "\n".join(main_readme_lines).format(
        paper_list=insertion_lines,
    )

    with open("README.md", "w") as f:
        f.write(result)


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

    with open(os.path.join(PAPER_DIR, arxiv_id, "paper.en.html"), "w") as f:
        f.write(en_result_html)

    ko_result_html_lines = html_lines[:6] + [wrap(line) for line in ko_mmd_lines] + html_lines[6:]
    ko_result_html = "\n".join(ko_result_html_lines)

    with open(os.path.join(PAPER_DIR, arxiv_id, "paper.ko.html"), "w") as f:
        f.write(ko_result_html)

    result_readme = "\n".join(readme_lines).format(
        title=".".join(en_mmd_fn.split("/")[-1].split(".")[:-1]).replace("_", " "),
        arxiv_url="https://arxiv.org/abs/{arxiv_id}".format(arxiv_id=arxiv_id),
        ar5iv_url="https://ar5iv.org/abs/{arxiv_id}".format(arxiv_id=arxiv_id),
        en_html_url="https://raw.githack.com/{github_id}/{repo_name}/master/papers/{arxiv_id}/paper.en.html".format(
            github_id=GITHUB_ID,
            repo_name=REPO_NAME,
            arxiv_id=arxiv_id,
        ),
        ko_html_url="https://raw.githack.com/{github_id}/{repo_name}/master/papers/{arxiv_id}/paper.ko.html".format(
            github_id=GITHUB_ID,
            repo_name=REPO_NAME,
            arxiv_id=arxiv_id,
        ),
    )

    with open(os.path.join(PAPER_DIR, arxiv_id, "README.md"), "w") as f:
        f.write(result_readme)


if __name__ == "__main__":
    en_mmd_fn = sys.argv[1]

    main(en_mmd_fn)
    update_main_readme()
