# {{ .Site.Title }}
> {{ .Site.Params.description }}

## Recent Posts
{{ range first 10 (where .Site.RegularPages "Section" "blog") }}
- [{{ .Title }}]({{ .RelPermalink }}): Published {{ .Date.Format "2006-01-02" }}
{{ end }}