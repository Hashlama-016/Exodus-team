#/bin/sh

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github-auth-rsa

REPOS="
git@github.com:Hashlama-016/airflow-DAGs.git
git@github.com:Hashlama-016/airflow-team-DAGs.git
git@github.com:Hashlama-016/Obelisk-DAGs.git
http://10.50.1.4/Hashlama_8/airflow-test.git
http://10.50.1.4/Hashlama_8/obelisk-airflow.git
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
