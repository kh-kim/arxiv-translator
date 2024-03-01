# Arxiv Translation Project

이 레포는 쏟아지는 페이퍼들에 대응하기 위하여, 빠르게 Arxiv 페이퍼를 살펴볼 수 있도록 한글화된 웹페이지를 제공하는 것을 목표로 합니다.
각기 다른 형태의 PDF 파일을 번역하기 위해서, 텍스트를 추출할 때 nougat OCR 라이브러리를 활용합니다.
따라서 추출이 원활하지 않을 수 있습니다.
처음에는 Ar5iv를 번역할까 생각했지만, Ar5iv도 한달이 지나서야 페이퍼가 업데이트 되며, 최초 버전만 HTML화 하고 최종 버전은 반영되어 있지 않기 때문에, 자체적으로 내용을 추출하기로 결정하였습니다.
정확한 내용을 파악하기 위해서는 원본 페이퍼를 읽는 것을 추천합니다.

## Paper List

새 창 열기가 지원되지 않습니다. 직접 새 창으로 열기를 통해 열기를 권장합니다.

| ArXiv ID | Title | ArXiv / Ar5iv | English / Korean |
|:--------:|-------|:-------------:|:----------------:|
| 2402.17764 | The Era of 1-bit LLMs All Large Language Models are in 158 Bits | [arXiv](https://arxiv.org/abs/2402.17764) / [ar5iv](https://ar5iv.org/abs/2402.17764) | [en](https://raw.githack.com/kh-kim/arxiv-translator/master/papers/2402.17764/paper.en.html) / [ko](https://raw.githack.com/kh-kim/arxiv-translator/master/papers/2402.17764/paper.ko.html) |
| 2402.14714 | Efficient and Effective Vocabulary Expansion Towards Multilingual Large Language Models | [arXiv](https://arxiv.org/abs/2402.14714) / [ar5iv](https://ar5iv.org/abs/2402.14714) | [en](https://raw.githack.com/kh-kim/arxiv-translator/master/papers/2402.14714/paper.en.html) / [ko](https://raw.githack.com/kh-kim/arxiv-translator/master/papers/2402.14714/paper.ko.html) |
| 2402.06196 | Large Language Models A Survey | [arXiv](https://arxiv.org/abs/2402.06196) / [ar5iv](https://ar5iv.org/abs/2402.06196) | [en](https://raw.githack.com/kh-kim/arxiv-translator/master/papers/2402.06196/paper.en.html) / [ko](https://raw.githack.com/kh-kim/arxiv-translator/master/papers/2402.06196/paper.ko.html) |

## Procedure

Arxiv 페이퍼를 번역하기 위해서 총 4단계를 거칩니다.

#### ArXiv Paper Download

Arxiv는 wget 등의 명령어를 통해서 pdf 파일을 다운로드 받을 수 없게 하였습니다.
아마도 무분별한 scrapping에 대응하기 위한 것으로 생각됩니다.
따라서 pdf 파일을 다운로드 받기 위해서 [arxiv-dl](https://pypi.org/project/arxiv-dl/) 패키지를 활용합니다.

#### PDF to Markdown

[Nougat OCR](https://github.com/facebookresearch/nougat)을 활용하여 Mathpix Markdown 파일로 변환합니다.

#### Translation

자체 번역 모델을 활용하여 번역을 수행합니다.
다음과 같이 페이퍼의 번역을 위해 사용된 번역기의 성능(초록색)은 DeepL과 Google, Naver의 중간쯤에 위치합니다.

![NMT Evaluation Results](assets/nmt_eval.png)

#### Markdown to HTML

Mathpix Markdown을 HTML로 변환합니다.
변환 방법은 [여기](https://github.com/Mathpix/mathpix-markdown-it/tree/master?tab=readme-ov-file#using-mathpix-markdown-it-in-web-browsers)에 설명되어 있습니다.
그리고 저장된 github에 push되어 저장된 HTML 파일을 githack.com을 통해 렌더링하도록 합니다.

## Future Work

페이퍼 중간의 이미지들은 Nougat OCR에서 추출해주지 않기 때문에 빠져 있습니다.
따라서 이미지도 함께 포함하여 결과물을 만들어내도록 하고자 합니다.

## Contact

Kim Ki Hyun
pointzz.ki@gmail.com