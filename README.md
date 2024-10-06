# War Crimes and Chill Discord Bot

## Overview

This Discord bot is designed for military-themed servers, providing a range of features to enhance user engagement, manage server operations, and facilitate communication. It includes an XP system, calendar integration, note-taking capabilities, and various other utilities.

## Features

1. **XP and Leveling System**
   - Multiple categories: Fitness, ACFT, Gaming, Weapons Qualification, Music, and Memes
   - Custom titles and badges for each category
   - Leaderboards for each category

2. **Calendar Integration**
   - View and manage events
   - Visual calendar display
   - Appointment scheduling

3. **Notes System**
   - AI-powered note organization
   - Streamlined note-taking process

4. **Onboarding System**
   - Automated nickname enforcement
   - Role assignment
   - Interactive server tour

5. **Server Customization**
   - Custom themes for different teams (Scouts, Infantry, Hangout)
   - Unique visual elements and GIFs

6. **NCO Management**
   - Exclusive NCO channels and permissions
   - NCO role request and approval system

7. **Sensitive Items and Property Accountability**
   - Link to external spreadsheet for equipment tracking

8. **Custom Commands**
   - `!setupserver`: Initializes the server layout
   - `!calendar`: Displays calendar options
   - `!notes`: Opens the notes interface
   - `!onboarding`: Shows onboarding options for new members
   - `!rank [category]`: Displays user rank and XP in a specific category
   - `!leaderboard`: Shows interactive leaderboard for different categories
   - `!profile`: Displays user profile with stats across categories

9. **Interactive UI Elements**
   - Button-based interactions for improved user experience

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/your-username/war-crimes-and-chill-bot.git
   cd war-crimes-and-chill-bot
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add the following variables:
     ```
     DISCORD_TOKEN=your_discord_bot_token
     OPENAI_API_KEY=your_openai_api_key
     GOOGLE_CALENDAR_CREDENTIALS_FILE=path_to_your_credentials_json_file
     ```

4. Set up Google Calendar API:
   - Follow the Google Calendar API setup instructions in the `google_calendar_setup.md` file

5. Customize the bot:
   - Modify `config.py` to set your server-specific settings
   - Add custom images to the `assets` folder as specified in the code

6. Run the bot:
   ```
   python bot.py
   ```

## Usage

Once the bot is running and invited to your server, use the following commands to interact with it:

- `!help`: Display all available commands
- `!setupserver`: Initialize the server layout (admin only)
- `!calendar`: Access calendar features
- `!notes`: Use the note-taking system
- `!onboarding`: Start the onboarding process for new members
- `!rank [category]`: Check your rank in a specific category
- `!leaderboard`: View leaderboards
- `!profile`: See your profile stats

## Contributing

Contributions are welcome! Please read the `CONTRIBUTING.md` file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers directly.