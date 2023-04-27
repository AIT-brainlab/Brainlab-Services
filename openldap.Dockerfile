FROM bitnami/openldap:2.6.4-debian-11-r20

COPY ./.ldappasswd /.ldappasswd
EXPOSE 389 636

# CMD tail -f /dev/null

USER 1001
ENTRYPOINT [ "/opt/bitnami/scripts/openldap/entrypoint.sh" ]
CMD [ "/opt/bitnami/scripts/openldap/run.sh" ]