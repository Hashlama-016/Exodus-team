# Exodus-team
Exodus Team - providing Airflow, NiFi and MLaas to Cloud services.


# Airflow
Airflow helm chart is taken from the official apache airflow helm chart at:  https://airflow.apache.org

## Changes to airflow helm chart ( values.yaml )
 * Changed all uid's to fit within the range limited by Openshift ( 1000800000 > )
 * Marked all instances of gid and fsGroup as comments to avoid errors thrown by Openshift
 * Marked all instances of runAsUser and uid in the postgres values file as comments to avoid errors thrown by Openshift ( Temporary change before switching to a managed instance of postgres )

 