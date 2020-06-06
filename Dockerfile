#  --- Base Image ---
FROM tiangolo/meinheld-gunicorn:python3.7 as base

#  --- DEPENDENCIES ---
FROM base AS dependencies

COPY ./forms_be/requirements.txt /app/forms_be/requirements.txt
RUN pip3 install --no-cache-dir -r  /app/forms_be/requirements.txt

# --- Copy Files/Build ---

FROM base AS release

WORKDIR /app
COPY ./forms_be /app
COPY .env-prod /app/forms_be/.env

COPY --from=dependencies /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/
COPY --from=dependencies /usr/local/bin/ /usr/local/bin/

ENV MODULE_NAME=forms_be.wsgi
ENV VARIABLE_NAME=application