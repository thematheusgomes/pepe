class CardMessages:
    def awslogs_exceptions(logGroup, filterName, count):
        return {
            "cards": [
              {
                "sections": [
                  {
                    "widgets": [
                      {
                        "textParagraph": {
                          "text": "<b>Service</b> <b><font color=\"#ff0000\">Error</font></b>"
                        }
                      }
                    ]
                  },
                  {
                    "widgets": [
                      {
                        "keyValue": {
                          "topLabel": "Environment",
                          "content": "PROD"
                        }
                      },
                      {
                        "keyValue": {
                          "topLabel": "Log Group",
                          "content": logGroup,
                          "button": {
                            "textButton": {
                              "text": "OPEN LOG GROUPS",
                              "onClick": {
                                "openLink": {
                                  "url": "https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/$252Fecs$252Fprod-fineract-api/log-events$3FfilterPattern$3D$2522org.apache.fineract.infrastructure.jobs.exception.JobExecutionException$2522$26start$3D-43200000"
                                }
                              }
                            }
                          }
                        }
                      },
                      {
                        "keyValue": {
                          "topLabel": "Filter Name",
                          "content": filterName
                        }
                      },
                      {
                        "keyValue": {
                          "topLabel": "Count Exceptions",
                          "content": count
                        }
                      }
                    ]
                  }
                ]
              }
            ]
          }

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
