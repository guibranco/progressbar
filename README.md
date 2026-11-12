# 🚀 Dynamic Progress Bar

Generates a **dynamic progress bar image** (SVG) using **Python**, deployed freely via **Vercel** — or [self-hosted](#-self-hosting) on your own server.

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
| `as_percent`            | With `scale`, show the number as a percentage of the scale                 | `false`               |
| `prefix`                | A string to add before the progress number                                 | None                  |
| `suffix`                | A string to add after the progress number                                  | `%`                   |
| `width`                 | The width of the progress bar in pixels                                    | `60` with a title, `90` without |
| `color`                 | The color of the title area (hex code without `#`)                         | `428bca` (blue)       |
| `progress_background`   | The background color of the progress bar (hex code without `#`)            | `555` (grey)          |
| `progress_number_color` | The color of the progress number (hex code without `#`)                    | `fff` (white)         |
| `progress_color`        | The color of the progress bar (hex code without `#`)                       | Depends on percentage |
| `show_text`             | Whether to display or hide the progress text                               | `true`                |
| `show_shadow`           | Whether to draw the text shadow                                            | `true`                |
| `radius`                | Corner radius in pixels                                                    | `4`                   |
| `style`                 | The style. One of: `default`, `flat`, `square`, `plastic`, `for-the-badge` | `default`             |
| `origin`                | Where the bar fills from: `left`, `center` (alias `middle`) or `right`. With `center`, zero is the middle of the bar — positive values grow right and negative values grow left (like Excel data bars) | `left` |
| `negative_color`        | Color of the bar for negative values (hex code without `#`). Overrides `progress_color` and the style color when the value is below zero | Depends on percentage |

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
| ![Progress from JSON](https://progress-bar.xyz/dynamic/json/?url=https%3A%2F%2Fraw.githubusercontent.com%2Fguibranco%2Fprogressbar%2Fmain%2Fdocs%2Fdynamic-json-sample.json&query=demo.metrics.translationPercent&title=JSON%20Demo) | [https://progress-bar.xyz/dynamic/json/?url=https%3A%2F%2Fraw.githubusercontent.com%2Fguibranco%2Fprogressbar%2Fmain%2Fdocs%2Fdynamic-json-sample.json&query=demo.metrics.translationPercent&title=JSON%20Demo](https://progress-bar.xyz/dynamic/json/?url=https%3A%2F%2Fraw.githubusercontent.com%2Fguibranco%2Fprogressbar%2Fmain%2Fdocs%2Fdynamic-json-sample.json&query=demo.metrics.translationPercent&title=JSON%20Demo) |
| ![Progress from JSON](https://progress-bar.xyz/dynamic/json/?url=https%3A%2F%2Fraw.githubusercontent.com%2Fguibranco%2Fprogressbar%2Fmain%2Fdocs%2Fdynamic-json-sample.json&query=demo.metrics.translationPercent) | [https://progress-bar.xyz/dynamic/json/?url=https%3A%2F%2Fraw.githubusercontent.com%2Fguibranco%2Fprogressbar%2Fmain%2Fdocs%2Fdynamic-json-sample.json&query=demo.metrics.translationPercent](https://progress-bar.xyz/dynamic/json/?url=https%3A%2F%2Fraw.githubusercontent.com%2Fguibranco%2Fprogressbar%2Fmain%2Fdocs%2Fdynamic-json-sample.json&query=demo.metrics.translationPercent) |

---

### ➖ Negative values and data bars

Negative numbers are accepted (e.g. `/-28/`). The bar length is the absolute value relative to `scale`, and the sign is kept in the text.
Use `origin=center` to get Excel-style data bars, which are handy for a column of positive and negative values in a Markdown table: each side of the middle axis spans `scale`.

| 📌 Preview | 🌐 URL |
| ---------- | ------ |
| ![Progress](https://progress-bar.xyz/-28/) | [https://progress-bar.xyz/-28/](https://progress-bar.xyz/-28/) |
| ![Progress](https://progress-bar.xyz/75/?origin=center&title=delta) | [https://progress-bar.xyz/75/?origin=center&title=delta](https://progress-bar.xyz/75/?origin=center&title=delta) |
| ![Progress](https://progress-bar.xyz/-40/?origin=center&title=delta) | [https://progress-bar.xyz/-40/?origin=center&title=delta](https://progress-bar.xyz/-40/?origin=center&title=delta) |
| ![Progress](https://progress-bar.xyz/-30/?origin=center&scale=50&width=120&progress_color=3b82f6&negative_color=d9534f&suffix=) | [https://progress-bar.xyz/-30/?origin=center&scale=50&width=120&progress_color=3b82f6&negative_color=d9534f&suffix=](https://progress-bar.xyz/-30/?origin=center&scale=50&width=120&progress_color=3b82f6&negative_color=d9534f&suffix=) |
| ![Progress](https://progress-bar.xyz/60/?origin=right&title=rtl) | [https://progress-bar.xyz/60/?origin=right&title=rtl](https://progress-bar.xyz/60/?origin=right&title=rtl) |

`origin` and `negative_color` also work with [`/dynamic/json/`](#-progress-from-a-json-url), so a negative number read from a JSON document renders the same way.

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

Sample JSON file:
[https://raw.githubusercontent.com/guibranco/progressbar/main/docs/dynamic-json-sample.json](https://raw.githubusercontent.com/guibranco/progressbar/main/docs/dynamic-json-sample.json)

Use query parameters:

| Parameter   | Description |
| ----------- | ----------- |
| **`url`**   | Required. Address of the JSON document (`http` or `https`). Must be URL-encoded in the query string. |
| **`query`** | Required. [JSONPath](https://goessner.net/articles/JsonPath/) (e.g. `$.items[0].metrics.pct`) or dot form from the root (e.g. `items.0.metrics.pct`). Filter expressions are supported, so you can look up a value by a sibling field instead of a hardcoded index — e.g. `$.progress[?(@.data.language.name=='Spanish')].data.translationProgress`. |
| **`cache`** | Optional. `Cache-Control` max-age in seconds (alias `cacheSeconds`), between `0` and `86400`. Default: `300`. `0` disables caching for that request. |

Any other parameters from the table above (`title`, `scale`, `style`, …) apply the same way as on `/{number}/`.

---

## ⚡ Caching

Badges are fetched by GitHub's image proxy (camo), browsers and CDNs on every README render, so every response carries a `Cache-Control` header:

| Route             | `Cache-Control`                                                                   |
| ----------------- | --------------------------------------------------------------------------------- |
| `/{number}/`      | `public, max-age=604800, s-maxage=604800, stale-while-revalidate=604800` — the SVG is fully determined by the URL, so it is safe to cache for a week |
| `/dynamic/json/`  | `public, max-age=300, s-maxage=300` by default; override per request with `cache=` |
| `/favicon.ico`    | `public, max-age=2592000, s-maxage=2592000, stale-while-revalidate=604800` (30 days) |
| Errors, `/health` | `no-store`                                                                        |

The two defaults can be changed per deployment with the environment variables `PROGRESSBAR_STATIC_CACHE_SECONDS` (0–2592000, default 7 days) and `PROGRESSBAR_DYNAMIC_CACHE_SECONDS` (0–86400). Keep in mind that changes to a badge's look can take up to the configured static TTL (7 days by default, up to 30 days if `PROGRESSBAR_STATIC_CACHE_SECONDS` is raised) to show up in READMEs — and a CDN that honours `stale-while-revalidate` may keep serving the previous version for up to another 7 days while it refreshes the entry in the background.

---

## 🚀 Deployment

### ▲ Vercel

Deploy this project to **Vercel** with a single click:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/import/project?template=https://github.com/guibranco/progressbar)

The Hobby plan counts every request (cached or not) against its monthly quota, so a popular badge can hit the limit and get the deployment paused. The `Cache-Control` headers above keep most renders away from Vercel; if that is still not enough, self-host it.

### 🏠 Self-hosting

The same code runs anywhere Python runs. The repository ships everything needed for a small VM (1 vCPU / 1 GB is plenty — the app is stateless and serves ~1.8 KB per badge in about a millisecond):

| File                                   | Purpose                                                                                   |
| -------------------------------------- | ----------------------------------------------------------------------------------------- |
| `Dockerfile`, `compose.yaml`           | gunicorn (threaded workers) on `127.0.0.1:8099`, non-root, with a Docker healthcheck       |
| `gunicorn.conf.py`                     | Sizing/logging knobs, all overridable via `PROGRESSBAR_*` environment variables (`deploy/env.example`) |
| `deploy/nginx/`                        | NGINX reverse proxy with a response cache (`proxy_cache`), so Python only runs on cache misses |
| `deploy/systemd/`                      | systemd units for the compose stack, or for bare-metal gunicorn without Docker            |
| `deploy/install.sh`, `deploy/update.sh`| First-time setup and redeploy scripts for the VM                                          |
| `.github/workflows/deploy.yml`         | Optional CI deploy over SSH after `CI` passes on `main` (opt-in via `SELF_HOST_DEPLOY=true`) |

Quick start on an Ubuntu host with Docker and NGINX installed (`DOMAIN=` and `APP_DIR=` can be exported first to override the defaults):

```sh
curl -fsSLO https://raw.githubusercontent.com/guibranco/progressbar/main/deploy/install.sh
less install.sh                            # review before running it as root
sudo bash install.sh
sudo certbot --nginx -d progress-bar.xyz   # TLS
```

Or without Docker:

```sh
python -m venv venv && venv/bin/pip install -r requirements.txt
venv/bin/gunicorn -c gunicorn.conf.py app:app   # http://127.0.0.1:8099/58/
```

`GET /health` returns `{"status": "ok"}` for uptime monitors and load balancers. Put the domain behind a CDN/proxy (for example Cloudflare's free plan) to get edge caching and to be able to switch origins without touching the app.

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
                <a href="https://github.com/nimble-turtle">
                    <img src="https://avatars.githubusercontent.com/u/190960520?v=4" width="100;" alt="nimble-turtle"/>
                    <br />
                    <sub><b>nimble-turtle</b></sub>
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
