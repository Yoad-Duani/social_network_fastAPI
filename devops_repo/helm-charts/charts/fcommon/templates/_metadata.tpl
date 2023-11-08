{{- define "fcommon.metadata" -}}
  name: {{ include "fcommon.names.fullname" . }}
labels:
  {{- include "fcommon.labels" . | nindent 2 -}}
{{- end -}}
