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
    p.add_argument("--ar5iv", action="store_true")
    p.add_argument("--html_base_dir", default="./papers/")

    return p.parse_args()

def read_html(fn):
    with open(fn, "r") as f:
        return f.read()
    
def write_html(fn, html):
    with open(fn, "w") as f:
        f.write(html)

def translate_html(html, arxiv_id, is_ar5iv=False):
    if not is_ar5iv: # ArXiv Native HTML
        if "<p>HTML is not available for the source.</p>" in html:
            raise ValueError(f"HTML is not available for the source: {arxiv_id}")

        # find "=/" and replace with "=\"https://arxiv.org/"
        html = html.replace("=\"/", "=\"https://arxiv.org/")

        # find r"src=\".*\.png\"" and replace with "src=\"https://arxiv.org/html/2402.06196v2/\1\""
        html = re.sub(r"src=\"(.*\.png)\"", "src=\"https://arxiv.org/html/" + arxiv_id + r"/\1" + "\"", html)

        # find "<nav class=\"ltx_TOC active\"" and replace with "<nav class=\"ltx_TOC mobile collapse\"".
        html = html.replace("<nav class=\"ltx_TOC active\"", "<nav class=\"ltx_TOC mobile collapse\"")
    else:
        html = html.replace("href=\"/", "href=\"https://ar5iv.labs.arxiv.org/")
        html = html.replace("src=\"/", "src=\"https://ar5iv.labs.arxiv.org/")

    translated_lines = []
    buffer = []
    tag_cnt_map = {}
    for line_idx, line in tqdm.tqdm(enumerate(html.split("\n"))):
        if line.startswith("<p class=\"ltx_p\"") or line.startswith("<figcaption") \
                or (line.startswith("<p id=") and "class=\"ltx_p\"" in line):
            # find html tag using re and count for each
            re_result = re.findall(r"<[^>]+>", line)
            for tag in re_result:
                if tag[1] == "/":
                    tag_type = tag[2:-1].split(" ")[0]
                    tag_cnt_map[tag_type] = tag_cnt_map.get(tag_type, 0) - 1

                    # assert tag_cnt_map[tag_type] >= 0, \
                    #     f"Error at line {line_idx}: {tag_type} tag count is negative in {arxiv_id}"
                else:
                    tag_type = tag[1:-1].split(" ")[0]
                    tag_cnt_map[tag_type] = tag_cnt_map.get(tag_type, 0) + 1

            buffer.append(line)
        elif buffer:
            re_result = re.findall(r"<[^>]+>", line)
            for tag in re_result:
                if tag[1] == "/":
                    tag_type = tag[2:-1].split(" ")[0]
                    tag_cnt_map[tag_type] = tag_cnt_map.get(tag_type, 0) - 1

                    # assert tag_cnt_map[tag_type] >= 0, \
                    #     f"Error at line {line_idx}: {tag} tag count is negative in {arxiv_id}"
                else:
                    tag_type = tag[1:-1].split(" ")[0]
                    tag_cnt_map[tag_type] = tag_cnt_map.get(tag_type, 0) + 1

            buffer.append(line)
        else:
            translated_lines.append(line)

        if tag_cnt_map.get("p", 0) == 0 and buffer:
            original_p = None
            original_figcaption = None

            a_list = []
            cite_list = []
            footnote_list = []
            math_list = []

            # if buffer is not empty, join buffer and append to translate_lines
            if buffer:
                src = " ".join(buffer)

                soup = bs(src, "html.parser")
                if soup.text.strip() == "":
                    translated_lines.append(src)
                    buffer = []
                    continue

                try:
                    # extract the content inside of <p class=\"ltx_p>...</p>, including all html tags
                    soup = bs(src, "html.parser")
                    for p in soup.find_all("p", class_="ltx_p"):
                        src = "".join(list(map(str, p.contents)))
                        original_p = str(p).split(str(p.contents[0]))[0]
                except:
                    print(f"Error at line {line_idx}: cannot parse <p> in {arxiv_id}")

                try:
                    # extract the content inside of <figcaption>...</figcaption>, including all html tags
                    soup = bs(src, "html.parser")
                    for figcaption in soup.find_all("figcaption"):
                        src = "".join(list(map(str, figcaption.contents)))
                        original_figcaption = str(figcaption).split(str(figcaption.contents[0]))[0]
                except:
                    print(f"Error at line {line_idx}: cannot parse <figcaption> in {arxiv_id}")

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

                # <cite>...</cite>
                soup = bs(src, "html.parser")
                for cite in soup.find_all("cite"):
                    cite_list.append(cite)
                for idx, cite in enumerate(cite_list):
                    src = src.replace(str(cite), f"<cite idx={idx}></cite>")

                # if src contains <a href>???</a>, replace with "<a></a>"
                # Note that <a> contains many other tags, so we need to consider it.
                # Note that before replacing, save the replace target to a list for restoring.                
                soup = bs(src, "html.parser")
                for a in soup.find_all("a"):
                    a_list.append(a)
                for idx, a in enumerate(a_list):
                    src = src.replace(str(a), f"<a idx={idx}></a>")

                # add heuristics logic to skip dirty lines
                if len(bs(" ".join(buffer), "html.parser").text) / len(" ".join(buffer)) < 0.08:
                    translated_lines.append(" ".join(buffer))

                    print()
                    print(original_p)
                    print(" ".join(buffer))
                    print(src)
                    print(len(" ".join(buffer)), len(bs(" ".join(buffer), "html.parser").text), len(bs(" ".join(buffer), "html.parser").text) / len(" ".join(buffer)))

                    buffer = []
                    continue

                # translate src
                tgt = translate_lines("enko_20230719", src, batch_size=32)
                # print(tgt)

                # restore <a>, <cite>, <span>, <math>
                for idx, a in enumerate(a_list):
                    try:
                        tgt = tgt.replace(f"<a idx={idx}></a>", str(a))
                    except:
                        print(f"Error at line {line_idx}: cannot restore <a> at idx={idx} in {arxiv_id}")
                for idx, cite in enumerate(cite_list):
                    try:
                        tgt = tgt.replace(f"<cite idx={idx}></cite>", str(cite))
                    except:
                        print(f"Error at line {line_idx}: cannot restore <cite> at idx={idx} in {arxiv_id}")
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

                if original_p:
                    tgt = str(original_p) + tgt + "</p>"
                if original_figcaption:
                    tgt = str(original_figcaption) + tgt + "</figcaption>"

                translated_lines.append(tgt)

            buffer = []
            tag_cnt_map = {}

    html = "\n".join(translated_lines)
    return html

if __name__ == "__main__":
    config = define_argparser()

    arxiv_id = config.arxiv_id
    fn = os.path.join(config.html_base_dir, arxiv_id, "paper.{type}.en.html".format(
        type="ar5iv" if config.ar5iv else "raw"
    ))

    html = read_html(fn)
    html = translate_html(html, arxiv_id, config.ar5iv)
    write_html(
        os.path.join(config.html_base_dir, arxiv_id, "paper.{type}.ko.html".format(
            type="ar5iv" if config.ar5iv else "raw"
        )),
        html
    )
