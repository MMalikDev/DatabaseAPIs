#!/bin/bash

# set -e

source ./scripts/reset.sh
# ---------------------------------------------------------------------- #
# Define Docker Variables
# ---------------------------------------------------------------------- #
declare -a images=(
    server_django
    server_fastapi
    server_express
    code_py
    code_js
    static
)
declare -a volumes=(
    development_redis_data
    development_mongo_data
    development_mongo_config
    development_pgadmin_data
    development_postgres_data
)
declare -a bindings=()

# ---------------------------------------------------------------------- #
# Main Function
# ---------------------------------------------------------------------- #
main(){
    # Shut down all containers
    docker compose down
    
    # End Reverse Proxy
    end_proxy
    
    # Clean up
    run folders remove_folders  ${bindings[*]}
    run volumes remove_volumes  ${volumes[*]}
    run images  remove_images   ${images[*]}
    
    prune_docker
}

main $@
