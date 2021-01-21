# README
### authentication section:
In this section we analyze the authentication and the credential of the users who have access to the Infected Users pool (IUP) and those who have access to send Request Transaction (RT).
The steps is in this order:

- User SignIn: If a user who want to have the premium access to the network should first sign in. There is a private document named authorized_users managed by the health care system managers which defines the authorized users.
if a user sign in process goes well his information will be save in the and the created IUP_managers table. These users can receive the enough credential to the parts of the application which need this credential.

- Receiving Credential: The users who are signed in successfully receive this credential.