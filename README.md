# Monitoring

## Steps
1. Create a data.json file or edit example.json in /services/app/ directory
2. Edit config.ini file
3. Edit .env.db and change user details
4. Run `docker compose up -d --build`

## Integrate PushSafer Notifications
1. Create a user at pushsafer.com
2. Copy and paste the API key in config.ini file:
   ```
    #PushSafer API configurations 
    [PUSH_SAFER]
    PUSH_URL= https://www.pushsafer.com
    #Enter your PushSafer API key
    PUSH_API_KEY= API_KEY_HERE
    #Enter your icon file path
    PUSH_ICON= logo.png
    ```
3. Add a device to pushsafer