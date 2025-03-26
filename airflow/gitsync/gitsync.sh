#/bin/sh

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github-auth-rsa

REPOS="
http://10.50.19.6/airflow/ares-airflow.git
http://10.50.19.6/airflow/zeus-airflow.git
git@github.com:Hashlama-016/airflow-team-DAGs.git
"

for repo in $REPOS; do
	set -- $repo
	URL=$1
	DIR=$(basename "$1")

	echo $URL
	echo $DIR

	if [ -z "$URL" ] || [ -z "$DIR" ]; then
		echo skipping
		continue
	fi

	if [ ! -d "/opt/airflow/dags/$DIR/.git" ]; then
		echo "Cloning $URL..."
		git clone --depth 1 "$URL" "/opt/airflow/dags/$DIR"
		git config --global --add safe.directory "/opt/airflow/dags/$DIR"
	else
		echo "Updating $URL..."
		cd "/opt/airflow/dags/$DIR" && git pull origin main
	fi
done
