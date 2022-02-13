[![Codacy Badge](https://app.codacy.com/project/badge/Grade/64cf77885d8442a9ac39389d3fcdf3cd)](https://www.codacy.com/gh/carboncopies/BrainGenix-UI/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=carboncopies/BrainGenix-UI&amp;utm_campaign=Badge_Grade)

# BrainGenix-UI
The BrainGenix Management API allows external programs to interact with the system. The Management API is responsible for the interaction between BrainGenix systems and the GUI/Web interface as well as the command line interface. Interactions from a client are sent through an intermediate API server which presents a unified interface across the BrainGenix platform. Authentication is handled during the connection progress, and a token is subsequently provided by the server.

# Additional Info
The backend folder contains the APIServer that interacts with the other three BrainGenix systems (NES, STS, ERS), while the frontend folder contains the web interface js and express server.
