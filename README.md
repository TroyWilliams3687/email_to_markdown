# Email to Markdown

## Introduction

THis program will take a set of MSG or EML message file formats and extract the text/HTML and write to Markdown format. In addition, the attachments will be extracted as well.

## Usage

```bash
$ emailmd extract

$ emailmd extract ~/email/*.msg ~/email/*.eml ~/email/output

$ emailmd extract ~/"path to email"/*.msg ~/email/output

$ emailmd extract ~/tmp/"email to markdown"/eml/* ~/tmp/"email to markdown"/msg/* ~/email/output

$ emailmd extract ~/tmp/"email to markdown"/eml/* ~/tmp/"email to markdown"/msg/* ~/tmp/"email to markdown"/output

```

### Make

## License

[MIT](https://choosealicense.com/licenses/mit/)

