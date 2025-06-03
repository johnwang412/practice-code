# Overview

Library book manager software
Can extend to management of other Library things, e.g., conference rooms

# Progress

Next steps
- Update the /app monolith service to just be the assets / items service and
    have it begin to interface with the user app

Created two apps
- app: initial monolith app with books and user entities
- app-user: separate user entity - goal was to create just a user service and
    have that interact with a assets / items entity that allows inventory
    management and checkout capabilities
