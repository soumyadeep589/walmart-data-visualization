export PYTHONPATH=${PROJDIR}:${PROJDIR}/

function pushd2() {
  PUSHED="$(pwd)"
  cd "$PROJDIR""$1" >>/dev/null
}

function popd2() {
  cd "${PUSHED:-"$PROJDIR"}" >>/dev/null
  unset PUSHED
}

function pyfmt() {
  black $PROJDIR
}

showmigrations() {
  manage showmigrations $*
}

function makemigrations() {
  manage makemigrations $*
}

function migrate() {
  manage migrate $*
}

function djshell() {
  manage shell_plus
}

function dbshell() {
  manage dbshell
}

function manage() {
  python manage.py $*
  r=$?
  popd2
  return ${r}
}


function recreatedb() {
  psql -h pg -U postgres -c "CREATE USER root IF NOT EXISTS;"
  psql -h pg -U postgres -c "ALTER USER root WITH SUPERUSER;"
  psql -h pg -c "DROP DATABASE IF EXISTS walmart;" template1
  psql -h pg -c "CREATE DATABASE walmart" template1
  migrate $*
}

function run_dj() {
  manage runserver 0.0.0.0:8000
}
