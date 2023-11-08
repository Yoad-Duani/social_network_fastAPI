# {{/*
# Expand the name of the chart.
# */}}
# {{- define "fcommon.name" -}}
# {{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
# {{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
# {{- define "fcommon.fullname" -}}
# {{- if .Values.fullnameOverride }}
# {{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
# {{- else }}
# {{- $name := default .Chart.Name .Values.nameOverride }}
# {{- if contains $name .Release.Name }}
# {{- .Release.Name | trunc 63 | trimSuffix "-" }}
# {{- else }}
# {{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
# {{- end }}
# {{- end }}
# {{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
# {{- define "fcommon.chart" -}}
# {{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
# {{- end }}

{{/*
Common labels
*/}}
# {{- define "fcommon.labels" -}}
# helm.sh/chart: {{ include "fcommon.chart" . }}
# {{ include "fcommon.selectorLabels" . }}
# {{- if .Chart.AppVersion }}
# app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
# {{- end }}
# app.kubernetes.io/managed-by: {{ .Release.Service }}
# {{- end }}

{{/*
Selector labels
*/}}
# {{- define "fcommon.selectorLabels" -}}
# app.kubernetes.io/name: {{ include "fcommon.name" . }}
# app.kubernetes.io/instance: {{ .Release.Name }}
# {{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "fcommon.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "fcommon.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}


{{- define "fcommon.deploymentStrategy" -}}
  {{- if .Values.deploymentStrategy -}}
strategy:
  type: {{ .Values.deploymentStrategy }}
  {{- end -}}
{{- end -}}


{{- define "fcommon.util.merge" -}}
{{- $top := first . -}}
{{- $overrides := fromYaml (include (index . 1)$top) | default (dict ) -}}
{{- $tpl := fromYaml (include (index . 2)$top) | default (dict ) -}}
{{- toYaml (merge $overrides $tpl) -}}
{{- end -}}

{{- define "fcommon.tplValue" -}}
  {{- if typeIs "string" .value -}}
    {{- tpl .value .context -}}
  {{- else -}}
    {{- tpl (.value | toYaml) .context -}}
  {{- end -}}
{{- end -}}

{{- define "fcommon.initContainersHealthcheckEndpoints" -}}
{{ range .Values.initContainersHealthcheckEndpoints }}
- name: wait-for-endpoint-{{ (split ":" .)._0 }}
  iamge: curlimage/curl:8.2.0
  args:
    - /bin/sh
    - -c
    - >
      set -x;
      while [ $(curl -sw '%{http_code}' "http://{{ $.Release.Name }}-{{ . }}" -o /dev/null) -ne 200 ]; do
        sleep 30;
      done
  resources:
    limits:
      memory: 64Mi
      cpu: 250m
{{- end -}}
{{- end -}}

