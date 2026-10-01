# {{ .Title }}
{{ with .Description }}> {{ . }}{{ end }}

{{ range .Pages }}
- [{{ .Title }}]({{ .RelPermalink }}): Published {{ .Date.Format "2006-01-02" }}
{{ end }}