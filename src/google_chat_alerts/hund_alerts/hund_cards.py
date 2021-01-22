class HundCardMessages:
     def health_check_alert(component_id, kind, color, message):
        return {
            "cards": [
                {
                    "sections": [
                        {
                            "widgets": [
                                {
                                    "textParagraph": {
                                        "text": f"<b>Component</b> <b><font color=\"{color}\">{kind.capitalize()}</font></b>"
                                    }
                                }
                            ]
                        },
                        {
                            "widgets": [
                                {
                                    "textParagraph": {
                                        "text": message
                                    }
                                }
                            ]
                        },
                        {
                            "widgets": [
                                {
                                    "buttons": [
                                        {
                                            "textButton": {
                                                "text": "COMPONENT STATUS",
                                                "onClick": {
                                                    "openLink": {
                                                        "url": f"https://status.boomcredit.net/components/{component_id}"
                                                    }
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
