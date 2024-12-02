# Backend Infrastructure (Repo 1)
Repo 1 of 2. This defines the AWS network infrastructure and backend components, and the associated Sentinel policies for each component. Frontend components are defined in repo 2.

The focus of this project was not the application code nor the Lambda function and as such there are several improvements that could be made.
I didn't implement HTTPS into my ALB as it wasn't in the scope of this project which is why inbound traffic to the ALB is over HTTP. I demonstrate practical use of tls certificates in a static site
cloudfront distribution in a different project.


The desired outcome of this project was to create an end-to-end CI/CD pipeline that automates deployment of a public facing web application and all of the associated cloud infrastructure.
There are several problems I aimed to solve with this project:
- Creating cloud infrastructure in such a way that it can be integrated with a version control provider like git and can be rapidly deployed. 
- Having a central location to store the state of said infrastructure
- Checking infrastructure prior to deployment to check for any misconfigurations - primarily those concerning security.
- Automating deployment of an application and maintaining security best practices (I cover this in repo 2)

Firstly, I used Terraform to achieve my version control and deployment goals. Terraform enables devs to define cloud infrastructure as code, using a declarative language - in this case HCL. 
It does so by utilizing a feature called state. Once infrastructure has been defined and then deployed, a state file is created and acts a blueprint to your current cloud infrastructure.Any subsequent changes to your IaC files are then compared against this state file to determine what changes need to be made to your cloud infrastructure. A potential issue, however, that comes with using IaC is state file management. If a development team doesn't work in a central location, Several members can quite quickly end up with different versions of state which would lead to issues when deploying. 

Now to remedy this, I used Terraform's cloud platform to manage state. It provides a single location that always holds the most up to date version of state, It offers state locking which prevents multiple infrastructure changes from happening at once and hence preventing state file corruption and, crucial to this project, easy integration with CI/CD pipelines. Once the statefile has been created I can access this statefile from a pipeline via the Terraform API to retrieve any outputs I need.

Infrastructure misconfigurations. A quick google search will tell you that roughly 82% of enterprises, 27% of businesses and 69% of organizations face security incidents or data breaches due to cloud misconfigurations. A very cheap a easy solution in avoiding these statistics is using Policy as Code. For this project I naturally used Sentinel - HCP's policy as code product - as it has built in support with Terraforms cloud platform. Now what policy as code does is it runs several functions (or rules) against the proposed changes to your infrastructure. These functions can be as specific or as general as required, they can check for security misconfigurations like overly permissive IAM policies across AWS resources, check for general resource configurations and more. The benefit this brings compared to it's cost is really a no brainer.


## AWS Components
- An **API-Gateway** with several, Lambda Intgrated methods

- A **Lambda function** with all of the associated API handlers

- A **virtual private cloud** with:
  - 2 public subnets
  - 2 private subnets
  - An internet gateway
  - An interface endpoint for Amazon Secrets Manager
  - Relevant route table associations

- 2 **RDS instances** running a MySQL database

- Security Groups allowing necessary traffic flows
    - ALB (Not defined in this repo): Inbound port 80 from 0.0.0.0/0 
    - Containers: Inbound port 80 from ALB-sg
    - Lambda: Outbound 443 to SSM-sg, Outbound 3306 to RDS-sg
    - SSM: Inbound 443 from Lambda
    - RDS: Stateful rule from Lambda - RDS-sg



## Sentinel Policies
Pushing code to this repo triggers a run in my first Terraform Cloud workspace. After a plan is created the following Sentinel policies are ran:
### Lambda
- Policies have access to too many resources (Resource == '*')
- Defined permissions are within an allowed list.
- Time-out is above a given threshold.

### RDS
- DB size is within allowed sizes.
- Storage encryption is enabled
- Default credentials are active
- DB instance is accessible from the internet.

### Secrets Manager
- Secrets rotation is enabled.
- Read replica is enabled.

### Security Groups
- If any sg is allows traffic from/to 0.0.0.0/0

### VPC 
- CIDR block prefix is within allowed sizing.
- Private subnet misconfigurations

