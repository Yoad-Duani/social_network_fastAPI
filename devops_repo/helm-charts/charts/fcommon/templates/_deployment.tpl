{{- define "fcommon.deployment.standard" -}}
{{- $metrics := .Values.metrics -}}
{{- $tz := .Values.global.timezone | default .Values.timezone -}}
apiVersion: apps/v1
kind: Deployment
metadata:
  {{- include "fcommon.metadata" . | nindent 2 -}}
  annotations:
    {{- include "fcommon.annotations.deployment" . | nindent 4 -}}
spec:
  {{- include "fcommon.deploymentStrategy" . | nindent 2 -}}
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "fcommon.labels.matchLabels" . | nindent 6 -}}
  template:
    metadata:
      annotations:
        {{- include "fcommon.annotations.pod" . | indent 8 -}}  # need to create annotations.pod
      labels:
        {{- include "fcommon.labels" . | nindent 8 -}}
    spec:
      {{- if .Values.serviceAccount.create -}}
      serviceAccount: {{ template "fcommon.names.fullname" }}
      {{- end -}}
      {{- if .Values.securityContext -}}
      securityContext:
      {{ toYaml .Values.securityContext | nindent 8 }}
      {{- end -}}
      {{- include "fcommon.imagePullSecrets" . | nindent 6 -}}
      {{ if or (.Values.initContainersHealthcheckEndpoints) (.Values.extraInitContainers) ($metrics.jmx.enabled) }}
      # initcontainers:
        # {{ if $metrics.jmx.enabled }}
        # - name: jmx-agent-artifact
        #   image: {{ .Values.global.jmxExporterJarImage }}  # need change all jmx to prometheus_client or any other exporter
        #   args:
        #     - /bin/sh
        #     - c
        #     - |
        #       ls -la . | grep jar
        #       cp *.jar /opt/jmx/
        #       cat <<EOF > /opt/jmx/jmx-config.yaml
        #       {{ $metrics.jmx.config | nindent 14 }}
        #       EOF
        #       ls -la /opt/jmx
        # volumeMounts:
        #   - name: jmx-folder
        #     mountPath: "/opt/jmx"
        # resources:
        #   limits:
        #     memory: "64Mi"
        #     cpu: "250m"
        # {{- end -}}
        # {{- if .Values.initContainersHealthcheckEndpoints -}}
        # {{- include "fcommon.initContainersHealthcheckEndpoints" | indent 8 -}}       
        # {{- end -}}
        # {{- if .Values.extraInitContainers -}}
        # {{ toYaml .Values.extraInitContainers | indent 8 }}
        # {{- end -}}
      {{- end -}}
      containers:
        - name: {{- include "fcommon.name" -}}
          image: {{- include "fcommon.image" -}}
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          {{- if .Values.command -}}
          command:
            {{ toYaml .Values.command | indent 10 }}
          {{- end -}}
          env:
          {{ if not .Values.coreService.enabled }}
            - name: server.contextPath
              value: {{ .Values.ingress.path }}
            {{- if .Values.ports.api -}}
            - name: server.port
              value: "{{ .Values.ports.api,containerPort }}"
            {{- end -}}
            - name: TZ
              value: "{{ $tz }}"
          {{- end -}}
          {{ $baseUrl := .Values.swaggerBaseUrl | default (first .Values.ingress.hosts) }}
            - name: swagger.baseUrl
              value: {{ .Values.global.swaggerBaseUrl | default $baseUrl }}
            - name: swagger.token.url
              value: "{{ .Values.global.swaggerTokenUrl | default .Values.swaggerTokenUrl }}"
          # {{- if .Values.coreService.enabled -}}
          # {{- end -}}
          {{- include "common.envFromSecret" .  | indent 12 -}}



      



{{- end -}}

