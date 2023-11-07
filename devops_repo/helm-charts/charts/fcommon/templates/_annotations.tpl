
{{- define "fcommon.annotations.basic" -}}
{{- with .Values.annotations -}}
{{ toYaml . }}
{{- end -}}
{{- end -}}

{{- define "fcommon.annotations.checksum" -}}
checksum/config: {{ include (print .TemplateBasePath "/configmao.yaml") . | sha256sum }}
{{- end -}}

{{- define "fcommon.annotations.deployment" -}}
{{- include "fcommon.annotations.basic" . -}}
{{- include "fcommon.annotations.checksum" . -}}
{{- range $key, $value := .Values.deployment.annotations -}}
{{ key }}: {{ include  "fcommon.tplValue" (dict "value" $value "contest" $ ) | quote }}
{{- end -}}
{{- end -}}