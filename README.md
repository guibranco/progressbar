# 🚀 Dynamic Progress Bar

Generates a **dynamic progress bar image** (SVG) using **Python**, deployed freely via **Vercel**.

📊 **Preview:**

![Progress](https://progress-bar.xyz/25/) ![Progress](https://progress-bar.xyz/50/) ![Progress](https://progress-bar.xyz/100/)

Inspired by [![fredericojordan/progress-bar](https://img.shields.io/badge/fredericojordan%2Fprogress--bar-black?style=flat&logo=github)](https://github.com/fredericojordan/progress-bar).

---

## 🔥 Other Projects

- ⭐ [![Star Rating](https://starrating-beta.vercel.app/5.0/)](https://github.com/GoulartNogueira/Star-Rating) **Dynamic Star Rating** - [![GoulartNogueira/Star-Rating](https://img.shields.io/badge/GoulartNogueira%2FStar--Rating-black?style=flat&logo=github)](https://github.com/GoulartNogueira/Star-Rating)

---

## 🛠️ Usage

This service is deployed on **[Vercel](https://vercel.com)** and accessible via the domain **[progress-bar.xyz](https://progress-bar.xyz)**.

---

## ⚙️ Parameters

| 🔧 Parameter            | 📜 Description                                                             | 🎯 Default Value      |
| ----------------------- | -------------------------------------------------------------------------- | --------------------- |
| `title`                 | Adds a title to the progress bar                                           | None                  |
| `scale`                 | The maximum value that the progress bar represents                         | 100                   |
| `prefix`                | A string to add before the progress number                                 | None                  |
| `suffix`                | A string to add after the progress number                                  | `%`                   |
| `width`                 | The width of the progress bar in pixels                                    | 100                   |
| `color`                 | The color of the progress bar (hex code without `#`)                       | `00ff00` (green)      |
| `progress_background`   | The background color of the progress bar (hex code without `#`)            | `ffffff` (white)      |
| `progress_number_color` | The color of the progress number (hex code without `#`)                    | `000000` (black)      |
| `progress_color`        | The color of the progress bar (hex code without `#`)                       | Depends on percentage |
| `show_text`             | Whether to display or hide the progress text                               | `true`                |
| `style`                 | The style. One of: `default`, `flat`, `square`, `plastic`, `for-the-badge` | `default`             |

### Examples

Below are several examples showcasing different ways to generate progress bars.

| 📌 Preview                                                                                                    | 🌐 URL                                                                                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ![Progress](https://progress-bar.xyz/28/)                                                                     | [https://progress-bar.xyz/28/](https://progress-bar.xyz/28/)                                                                                                                                         |
| ![Progress](https://progress-bar.xyz/28/?title=progress)                                                      | [https://progress-bar.xyz/28/?title=progress](https://progress-bar.xyz/28/?title=progress)                                                                                                           |
| ![Progress](https://progress-bar.xyz/58/)                                                                     | [https://progress-bar.xyz/58/](https://progress-bar.xyz/58/)                                                                                                                                         |
| ![Progress](https://progress-bar.xyz/58/?title=completed)                                                     | [https://progress-bar.xyz/58/?title=completed](https://progress-bar.xyz/58/?title=completed)                                                                                                         |
| ![Progress](https://progress-bar.xyz/91/)                                                                     | [https://progress-bar.xyz/91/](https://progress-bar.xyz/91/)                                                                                                                                         |
| ![Progress](https://progress-bar.xyz/91/?title=done)                                                          | [https://progress-bar.xyz/91/?title=done](https://progress-bar.xyz/91/?title=done)                                                                                                                   |
| ![Progress](https://progress-bar.xyz/180/?scale=10&title=mark&prefix=R$&suffix=)                              | [https://progress-bar.xyz/180/?scale=10&title=mark&prefix=R$&suffix=](https://progress-bar.xyz/180/?scale=10&title=mark&prefix=R$&suffix=)                                                           |
| ![Progress](https://progress-bar.xyz/420/?scale=500&title=funds&width=200&color=babaca&prefix=R$&suffix=)     | [https://progress-bar.xyz/420/?scale=500&title=funds&width=200&color=babaca&prefix=R$&suffix=](https://progress-bar.xyz/420/?scale=500&title=funds&width=200&color=babaca&prefix=R$&suffix=)         |
| ![Progress](https://progress-bar.xyz/7/?scale=10&title=mark&suffix=X)                                         | [https://progress-bar.xyz/7/?scale=10&title=mark&suffix=X](https://progress-bar.xyz/7/?scale=10&title=mark&suffix=X)                                                                                 |
| ![Progress](https://progress-bar.xyz/420/?scale=500&title=funds&width=200&color=babaca&suffix=$)              | [https://progress-bar.xyz/420/?scale=500&title=funds&width=200&color=babaca&suffix=$](https://progress-bar.xyz/420/?scale=500&title=funds&width=200&color=babaca&suffix=$)                           |
| ![Progress](https://progress-bar.xyz/58/?title=colorful&progress_background=ffc0cb&progress_number_color=000) | [https://progress-bar.xyz/58/?title=colorful&progress_background=ffc0cb&progress_number_color=000](https://progress-bar.xyz/58/?title=colorful&progress_background=ffc0cb&progress_number_color=000) |
| ![Progress](https://progress-bar.xyz/100/?progress_color=ff3300)                                              | [https://progress-bar.xyz/100/?progress_color=ff3300](https://progress-bar.xyz/100/?progress_color=ff3300)                                                                                             |
| ![Progress](https://progress-bar.xyz/100/?width=100&title=Fixed+color&progress_color=ff3300)                  | [https://progress-bar.xyz/100/?width=100&title=Fixed+color&progress_color=ff3300](https://progress-bar.xyz/100/?width=100&title=Fixed+color&progress_color=ff3300)                                     |
| ![Progress](https://progress-bar.xyz/28/?show_text=false)                                                     | [https://progress-bar.xyz/28/?show_text=false](https://progress-bar.xyz/28/?show_text=false)                                                                                                         |
| ![Progress](https://progress-bar.xyz/90/?show_text=false)                                                     | [https://progress-bar.xyz/90/?show_text=false](https://progress-bar.xyz/90/?show_text=false)                                                                                                         |

---

## 🎨 Styles

We currently support:

| 🎨 Style              | 📌 Preview                                                     | 🌐 URL                                                                                                 |
| --------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| 🟢 **flat** (default) | ![Progress](https://progress-bar.xyz/100/?style=flat)          | [https://progress-bar.xyz/100/?style=flat](https://progress-bar.xyz/100/?style=flat)                   |
| 🔲 **square**         | ![Progress](https://progress-bar.xyz/100/?style=square)        | [https://progress-bar.xyz/100/?style=square](https://progress-bar.xyz/100/?style=square)               |
| 🛡️ **plastic**        | ![Progress](https://progress-bar.xyz/100/?style=plastic)       | [https://progress-bar.xyz/100/?style=plastic](https://progress-bar.xyz/100/?style=plastic)             |
| 🔖 **for-the-badge**  | ![Progress](https://progress-bar.xyz/100/?style=for-the-badge) | [https://progress-bar.xyz/100/?style=for-the-badge](https://progress-bar.xyz/100/?style=for-the-badge) |
| 🎭 **thin-rounded** (WIP) | ![Progress](https://progress-bar.xyz/100/?style=thin-rounded)  | [https://progress-bar.xyz/100/?style=thin-rounded](https://progress-bar.xyz/100/?style=thin-rounded)   |
| 🪞 **neo-glass** (WIP) | ![Progress](https://progress-bar.xyz/100/?style=neo-glass)     | [https://progress-bar.xyz/100/?style=neo-glass](https://progress-bar.xyz/100/?style=neo-glass)         |
| 🎨 **minimal-matte** (WIP) | ![Progress](https://progress-bar.xyz/100/?style=minimal-matte) | [https://progress-bar.xyz/100/?style=minimal-matte](https://progress-bar.xyz/100/?style=minimal-matte) |

---

## 📡 Progress from a JSON URL

Besides a fixed value in the path (`/75/`), you can load the number from a remote JSON file.

**Example** (using the sample file in `docs/dynamic-json-sample.json`):

```txt
https://progress-bar.xyz/dynamic/json/?url=https%3A%2F%2Fraw.githubusercontent.com%2Fguibranco%2Fprogressbar%2Fmain%2Fdocs%2Fdynamic-json-sample.json&query=demo.metrics.translationPercent&title=JSON%20Demo
```

Sample JSON file:
[https://raw.githubusercontent.com/guibranco/progressbar/main/docs/dynamic-json-sample.json](https://raw.githubusercontent.com/guibranco/progressbar/main/docs/dynamic-json-sample.json)

![Progress from JSON](https://progress-bar.xyz/dynamic/json/?url=https%3A%2F%2Fraw.githubusercontent.com%2Fguibranco%2Fprogressbar%2Fmain%2Fdocs%2Fdynamic-json-sample.json&query=demo.metrics.translationPercent&title=demo)

Use query parameters:

| Parameter   | Description |
| ----------- | ----------- |
| **`url`**   | Required. Address of the JSON document (`http` or `https`). Must be URL-encoded in the query string. |
| **`query`** | Required. [JSONPath](https://goessner.net/articles/JsonPath/) (e.g. `$.items[0].metrics.pct`) or dot form from the root (e.g. `items.0.metrics.pct`). |
| **`cache`** | Optional. `Cache-Control` max-age in seconds. |

Any other parameters from the table above (`title`, `scale`, `style`, …) apply the same way as on `/{number}/`.

---

## 🚀 Deployment

Deploy this project to **Vercel** with a single click:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/import/project?template=https://github.com/guibranco/progressbar)

---

## 🤝 Contributing

Check out [CONTRIBUTING.md](CONTRIBUTING.md) to learn how to contribute!

### 👥 Contributors

<!-- readme: collaborators,contributors,snyk-bot/- -start -->
<table>
	<tbody>
		<tr>
            <td align="center">
                <a href="https://github.com/guibranco">
                    <img src="https://avatars.githubusercontent.com/u/3362854?v=4" width="100;" alt="guibranco"/>
                    <br />
                    <sub><b>Guilherme Branco Stracini</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/ztest95">
                    <img src="https://avatars.githubusercontent.com/u/110767420?v=4" width="100;" alt="ztest95"/>
                    <br />
                    <sub><b>ztest95</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/Pointbr8ker-123">
                    <img src="https://avatars.githubusercontent.com/u/153815372?v=4" width="100;" alt="Pointbr8ker-123"/>
                    <br />
                    <sub><b>David Nwosu</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/EduardoBaptista01">
                    <img src="https://avatars.githubusercontent.com/u/65791384?v=4" width="100;" alt="EduardoBaptista01"/>
                    <br />
                    <sub><b>Eduardo Baptista</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/bhosley">
                    <img src="https://avatars.githubusercontent.com/u/22378319?v=4" width="100;" alt="bhosley"/>
                    <br />
                    <sub><b>bhosley</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/nimble-turtle">
                    <img src="https://avatars.githubusercontent.com/u/190960520?v=4" width="100;" alt="nimble-turtle"/>
                    <br />
                    <sub><b>nimble-turtle</b></sub>
                </a>
            </td>
		</tr>
	</tbody>
</table>
<!-- readme: collaborators,contributors,snyk-bot/- -end -->

### 🤖 Bots

<!-- readme: bots,snyk-bot -start -->
<table>
	<tbody>
		<tr>
            <td align="center">
                <a href="https://github.com/dependabot[bot]">
                    <img src="https://avatars.githubusercontent.com/in/29110?v=4" width="100;" alt="dependabot[bot]"/>
                    <br />
                    <sub><b>dependabot[bot]</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/github-actions[bot]">
                    <img src="https://avatars.githubusercontent.com/in/15368?v=4" width="100;" alt="github-actions[bot]"/>
                    <br />
                    <sub><b>github-actions[bot]</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/penify-dev[bot]">
                    <img src="https://avatars.githubusercontent.com/in/399279?v=4" width="100;" alt="penify-dev[bot]"/>
                    <br />
                    <sub><b>penify-dev[bot]</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/deepsource-autofix[bot]">
                    <img src="https://avatars.githubusercontent.com/in/57168?v=4" width="100;" alt="deepsource-autofix[bot]"/>
                    <br />
                    <sub><b>deepsource-autofix[bot]</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/snyk-bot">
                    <img src="https://avatars.githubusercontent.com/u/19733683?v=4" width="100;" alt="snyk-bot"/>
                    <br />
                    <sub><b>Snyk bot</b></sub>
                </a>
            </td>
		</tr>
	</tbody>
</table>
<!-- readme: bots,snyk-bot -end -->

---

## 📜 License

This project is licensed under the **MIT License**.

📄 See [LICENSE](LICENSE) for details.
