{{- /*
  A post as Markdown, for AI crawlers and anyone who wants the text without
  the page around it. Front matter is replaced by a short header carrying
  the facts a reader needs to cite it. Image references are relative, so
  they resolve against this file's URL just as they do in the HTML.
*/ -}}
# {{ .Title }}

By {{ site.Params.author.name }} · {{ .Date.Format "January 2, 2006" }} · {{ .Permalink }}
{{- with .Description }}

> {{ . }}
{{- end }}

{{ .RenderShortcodes | strings.TrimSpace }}
