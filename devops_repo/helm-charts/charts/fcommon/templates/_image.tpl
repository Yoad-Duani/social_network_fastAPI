
{{- define "fcommon.imagePullSecrets" -}}
  {{- if .Values.global -}}
    {{- if .Values.global.imagePullSecrets -}}
imagePullSecrets:
      {{- range .Values.global.imagePullSecrets -}}
  - name: {{ . }}
      {{- end -}}
    {{- else if or .Values.image.pullSecrets -}}
imagePullSecrets:
      {{- range .Values.global.pullSecrets -}}
  - name: {{ . }}
      {{- end -}}
    {{- end -}}
  {{- end -}}
{{- end -}}

{{- define "fcommon.image" -}}
{{- $registryNmae := .Values.image.registry -}}
{{- $repositoryName := .Values.image.repository -}}
{{- $imageVersion := .Values.image.tag -}}
{{- if .Values.global.imageRegistry -}}
  $tmp := set . "imageRegistry" .Values.global.imageRegistry
{{- else -}}
  $tmp := set . "imageRegistry" .Values.image.registry
{{- end -}}
{{- if and .Values.global.imageVersion .Values.image.tagGlobalOverride -}}
  $tmp := set . "imageVersion" .Values.global.imageVersion
{{- else -}}
  $tmp := set . "imageVersion" .Values.image.tag
{{- end -}}
{{- printf "%s/%s:" .imageRegistry $repositoryName -}}{{ lower .imageVersion }}
{{- end -}}