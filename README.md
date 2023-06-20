# ogithub-actions
Openergy's Github Actions libraries

## maintenance
if an action must be modified:
- it should be versioned in order to ensure working workflows
- deprecation warning must be implemented in old actions
- workflow should also be versioned:
    - new workflow points on new action while we let the old workflow pointing on old action
    
This versioning is important so that all Openergy's github actions are always operational 