
{{- define "fcommon.labels.standard" -}}
{{- include "common.labels.standard" . -}}
{{- end -}}

{{- define "fcommon.labels.matchLabels" -}}
app.kubernetes.io/name: {{ include "common.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{- define "fcommon.labels.basic" -}}
{{ include "fcommon.util.merge" (list . "fcommon.labels.standard" "fcommon.labels.matchLabels") }}
{{- end -}}

{{- define "fcommon.labels.valuesLabels" -}}
      {{- with .Values.labels -}}
      {{- toYaml. | indent 8 -}}
      {{- end -}}
{{- end -}}

{{- define "fcommon.labels" -}}
{{ include "fcommon.util.merge" (list . "fcommon.labels.valuesLabels" "fcommon.labels.basic") }}
{{- end -}}