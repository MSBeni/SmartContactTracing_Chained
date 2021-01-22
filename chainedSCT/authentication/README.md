# README
### authentication section:
In this section we analyze the authentication and the credential of the users who have access to the Infected Users pool (IUP) and those who have access to send Request Transaction (RT).
The steps is in this order:

- User SignIn: If a user who want to have the premium access to the network should first sign in. There is a private document named authorized_users managed by the health care system managers which defines the authorized users.
if a user sign in process goes well his information will be save in the and the created IUP_managers table. These users can receive the enough credential to the parts of the application which need this credential.

- Receiving Credential: The users who are signed in successfully receive this credential.

- Tables description:
    - authorized_users private document: Defined the authorized users who are eligible to access some specific section of 
    application and can also send the Request Transaction (RT) and check the Infected Users pool (IUP).
    - authcheck table: The table which read ans save the IUP_authorized users to ca able to query.
    - iupmanagers table: The users who log in successfully and their access is approved by the system, will defined in this table and they
    will receive a token to have access to other specific section of the application which needs access token.
 
#### iup managers: 
- These users are defined and approved via authentication process and are defined in iupmanagers table.
The insert queries will be admitted by an authorized Infeceted Users Pool (IUP), which keep the record of the all
infected users. IUP will send another transaction in support of a user claim and the mining nodes by considering will
mine the block. 
- Consider that user X is infected with corona virus and is now a COVID-19 patient. A COVID-19 positive
document will be sent to the IUP and will be inserted into that database by the corresponding health officials. 
This pool is connected to the BSCTS and will share the approval infection transaction with the network.
-  The mining nodes are the authorized health and management centers who have access to the infeceted users pool (IUP).