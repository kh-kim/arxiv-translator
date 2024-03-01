import sys
import re
import tqdm
import argparse
import os

from bs4 import BeautifulSoup as bs

sys.path.append("/home/khkim/workspace/original_tech_demo")

from translate import translate_lines


def define_argparser():
    p = argparse.ArgumentParser()
    
    p.add_argument("--arxiv_id", required=True)
    p.add_argument("--html_base_dir", default="./papers/")

    return p.parse_args()

def read_html(fn):
    with open(fn, "r") as f:
        return f.read()
    
def write_html(fn, html):
    with open(fn, "w") as f:
        f.write(html)

def translate_html(html, arxiv_id):
    # find "=/" and replace with "=\"https://arxiv.org/"
    html = html.replace("=\"/", "=\"https://arxiv.org/")

    # find r"src=\".*\.png\"" and replace with "src=\"https://arxiv.org/html/2402.06196v2/\1\""
    html = re.sub(r"src=\"(.*\.png)\"", "src=\"https://arxiv.org/html/" + arxiv_id + r"/\1" + "\"", html)

    translated_lines = []
    buffer = []
    for line_idx, line in tqdm.tqdm(enumerate(html.split("\n"))):
        # if line starts with "<p class="ltx_p", add line to buffer
        if line.startswith("<p class=\"ltx_p\""):
            buffer.append(line)
        # if buffer is not empty and line not starts with "<", add line to buffer
        elif buffer and not line.startswith("<"):
            buffer.append(line)
        else:
            original_p = None
            a_list = []
            footnote_list = []
            math_list = []

            # if buffer is not empty, join buffer and append to translate_lines
            if buffer:
                src = " ".join(buffer)

                # extract the content inside of <p class=\"ltx_p>...</p>, including all html tags
                soup = bs(src, "html.parser")
                for p in soup.find_all("p", class_="ltx_p"):
                    src = "".join(list(map(str, p.contents)))
                    original_p = str(p).split(str(p.contents[0]))[0]

                # if src contains <math>???</math>, replace with "<math></math>"
                # Note that <math> contains many other tags, so we need to consider it.
                # Note that before replacing, save the replace target to a list for restoring.
                soup = bs(src, "html.parser")
                for math in soup.find_all("math"):
                    math_list.append(math)
                for idx, math in enumerate(math_list):
                    src = src.replace(str(math), f"<math idx={idx}></math>")

                # if src contains <span class="ltx_note ltx_role_footnote">???</span>, replace with "<span></span>"
                # In <span>, there are many other tags, so we need to consider it.
                # Note that before replacing, save the replace target to a list for restoring.
                soup = bs(src, "html.parser")
                for footnote in soup.find_all("span", class_="ltx_note ltx_role_footnote"):
                    footnote_list.append(footnote)
                for idx, footnote in enumerate(footnote_list):
                    src = src.replace(str(footnote), f"<span idx={idx}></span>")

                # if src contains <a href>???</a>, replace with "<a></a>"
                # Note that <a> contains many other tags, so we need to consider it.
                # Note that before replacing, save the replace target to a list for restoring.                
                soup = bs(src, "html.parser")
                for a in soup.find_all("a"):
                    a_list.append(a)
                for idx, a in enumerate(a_list):
                    src = src.replace(str(a), f"<a idx={idx}></a>")

                # translate src
                tgt = translate_lines("enko_20230719", src, batch_size=32)

                # restore <a>, <span>, <math>
                for idx, a in enumerate(a_list):
                    try:
                        tgt = tgt.replace(f"<a idx={idx}></a>", str(a))
                    except:
                        print(f"Error at line {line_idx}: cannot restore <a> at idx={idx} in {arxiv_id}")
                for idx, footnote in enumerate(footnote_list):
                    try:
                        tgt = tgt.replace(f"<span idx={idx}></span>", str(footnote))
                    except:
                        print(f"Error at line {line_idx}: cannot restore <span> at idx={idx} in {arxiv_id}")
                for idx, math in enumerate(math_list):
                    try:
                        tgt = tgt.replace(f"<math idx={idx}></math>", str(math))
                    except:
                        print(f"Error at line {line_idx}: cannot restore <math> at idx={idx} in {arxiv_id}")

                tgt = str(original_p) + tgt + "</p>"

                translated_lines.append(tgt)

            buffer = []

            translated_lines.append(line)

    html = "\n".join(translated_lines)
    return html

if __name__ == "__main__":
    config = define_argparser()

    arxiv_id = config.arxiv_id
    fn = os.path.join(config.html_base_dir, arxiv_id, "paper.raw.en.html")

    html = read_html(fn)
    html = translate_html(html, arxiv_id)
    write_html(
        os.path.join(config.html_base_dir, arxiv_id, "paper.raw.ko.html"),
        html
    )
