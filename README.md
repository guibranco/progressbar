# Dynamic Progress Bar

Generates a dynamic progress bar image (SVG) using Python, which is deployed freely via Vercel.

![Progress](https://progress-bar.xyz/25/) ![Progress](https://progress-bar.xyz/50/) ![Progress](https://progress-bar.xyz/100/) 

Inspired by [![fredericojordan/progress-bar](https://img.shields.io/badge/fredericojordan%2Fprogress--bar-black?style=flat&logo=github)](https://github.com/fredericojordan/progress-bar).

---

## Other projects

- [![Star Rating](https://starrating-beta.vercel.app/5.0/)](https://github.com/GoulartNogueira/Star-Rating) Dynamic Star Rating - [![GoulartNogueira/Star-Rating](https://img.shields.io/badge/GoulartNogueira%2FStar--Rating-black?style=flat&logo=github)](https://github.com/GoulartNogueira/Star-Rating)

---

## Usage

This service is deployed on [Vercel](https://vercel.com) and accessible via the domain [progress-bar.xyz](https://progress-bar.xyz).

---

## Parameters

| Parameter                | Description                                                                            | Default Value         |
|--------------------------|----------------------------------------------------------------------------------------|-----------------------|
| `title`                  | Adds a title to the progress bar                                                       | None                  |
| `scale`                  | The maximum value that the progress bar represents                                     | 100                   |
| `prefix`                 | A string to add before the progress number                                             | None                  |
| `suffix`                 | A string to add after the progress number                                              | %                     |
| `width`                  | The width of the progress bar in pixels                                                | 100                   |
| `color`                  | The color of the progress bar (hex code without `#`)                                   | `00ff00` (green)      |
| `progress_background`    | The background color of the progress bar (hex code without `#`)                        | `ffffff` (white)      |
| `progress_number_color`  | The color of the progress number (hex code without `#`)                                | `000000` (black)      |
| `progress_color`         | The color of the progress bar (hex code without `#`)                                   | Depends on calculated percentage |
| `show_text`              | If should display or hide the progress text                                            | `true`                |
| `style`                  | The style. One of: `default`, `flat`, `square`, `plastic`, `for-the-badge`             | `default`             |


---

## Examples

Below are several examples showcasing different ways to generate progress bars.

| Example Preview                                                                 | URL                                                                               |
|---------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| ![Progress](https://progress-bar.xyz/28/)                                       | [https://progress-bar.xyz/28/](https://progress-bar.xyz/28/)                      |
| ![Progress](https://progress-bar.xyz/28/?title=progress)                        | [https://progress-bar.xyz/28/?title=progress](https://progress-bar.xyz/28/?title=progress) |
| ![Progress](https://progress-bar.xyz/58/)                                       | [https://progress-bar.xyz/58/](https://progress-bar.xyz/58/)                      |
| ![Progress](https://progress-bar.xyz/58/?title=completed)                       | [https://progress-bar.xyz/58/?title=completed](https://progress-bar.xyz/58/?title=completed) |
| ![Progress](https://progress-bar.xyz/91/)                                       | [https://progress-bar.xyz/91/](https://progress-bar.xyz/91/)                      |
| ![Progress](https://progress-bar.xyz/91/?title=done)                            | [https://progress-bar.xyz/91/?title=done](https://progress-bar.xyz/91/?title=done) |
| ![Progress](https://progress-bar.xyz/180/?scale=10&title=mark&prefix=R$&suffix=)| [https://progress-bar.xyz/180/?scale=10&title=mark&prefix=R$&suffix=](https://progress-bar.xyz/180/?scale=10&title=mark&prefix=R$&suffix=) |
| ![Progress](https://progress-bar.xyz/420/?scale=500&title=funds&width=200&color=babaca&prefix=R$&suffix=) | [https://progress-bar.xyz/420/?scale=500&title=funds&width=200&color=babaca&prefix=R$&suffix=](https://progress-bar.xyz/420/?scale=500&title=funds&width=200&color=babaca&prefix=R$&suffix=) |
| ![Progress](https://progress-bar.xyz/7/?scale=10&title=mark&suffix=X)           | [https://progress-bar.xyz/7/?scale=10&title=mark&suffix=X](https://progress-bar.xyz/7/?scale=10&title=mark&suffix=X) |
| ![Progress](https://progress-bar.xyz/420/?scale=500&title=funds&width=200&color=babaca&suffix=$) | [https://progress-bar.xyz/420/?scale=500&title=funds&width=200&color=babaca&suffix=$](https://progress-bar.xyz/420/?scale=500&title=funds&width=200&color=babaca&suffix=$) |
| ![Progress](https://progress-bar.xyz/58/?title=colorful&progress_background=ffc0cb&progress_number_color=000) | [https://progress-bar.xyz/58/?title=colorful&progress_background=ffc0cb&progress_number_color=000](https://progress-bar.xyz/58/?title=colorful&progress_background=ffc0cb&progress_number_color=000) |
| ![Progress](https://progress-bar.xyz/100/?progress_color=ff3300) | [https://progress-bar.xyz/58/?progress_color=ff3300](https://progress-bar.xyz/58/?progress_color=ff3300) |
| ![Progress](https://progress-bar.xyz/100/?width=100&title=Fixed+color&progress_color=ff3300) | [https://progress-bar.xyz/58/?width=100&title=Fixed+color&progress_color=ff3300](https://progress-bar.xyz/58/?width=100&title=Fixed+color&progress_color=ff3300) |
| ![Progress](https://progress-bar.xyz/28/?show_text=false)                       | [https://progress-bar.xyz/28/?show_text=false](https://progress-bar.xyz/28/?show_text=false)      |
| ![Progress](https://progress-bar.xyz/90/?show_text=false)                       | [https://progress-bar.xyz/90/?show_text=false](https://progress-bar.xyz/90/?show_text=false)      |

---

## Styles

We currently have `flat` (default), `square` and `plastic` styles:

| Example Preview                                                                 | URL                                                                                      |
|---------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| ![Progress](https://progress-bar.xyz/100/?style=flat)                           | [https://progress-bar.xyz/100/?style=flat](https://progress-bar.xyz/100/?style=flat)     |
| ![Progress](https://progress-bar.xyz/100/?style=square)                         | [https://progress-bar.xyz/100/?style=square](https://progress-bar.xyz/100/?style=square) |   
| ![Progress](https://progress-bar.xyz/100/?style=plastic)                         | [https://progress-bar.xyz/100/?style=plastic](https://progress-bar.xyz/100/?style=plastic) |   

---

## Deployment

You can deploy this project to Vercel with a single click:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/import/project?template=https://github.com/guibranco/progressbar)

---

## License

This project is open-source and available under the MIT License.
