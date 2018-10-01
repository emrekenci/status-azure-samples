from applicationinsights import TelemetryClient
import json
import sys

# The below is your instrumentation key.
# You can find that on the properties blade of your app insights instance on Azure portal.
app_insights_client = TelemetryClient('<YOUR-INSTRUMENTATION-KEY>')

class custom_log_object():
    pass
    
def write_log(text_log):
    app_insights_client.track_event(text_log)

    # The flush statement sends all the telemetry in memory to the server.
    # Allow reducing HTTP overhead by grouping logs.
    app_insights_client.flush()

# Writing a custom log to application insights.
def write_custom_log(log_entry_name, log_entry):
    # Init a dictionary. the SDK requires the custom properties to be sent in a dict.
    log_properties = dict()

    # Fill the dictionary with objects properties
    for object_property in log_entry.__dict__ :
        log_properties[object_property] = getattr(log_entry, object_property)

    app_insights_client.track_event(log_entry_name, log_properties)
    app_insights_client.flush()

def exception_handling_sample():
    try:
        raise Exception("Exception message ABCD")
    except:
        app_insights_client.track_exception(sys.exc_info())
        app_insights_client.flush()

info_log = custom_log_object()
info_log.location = "hong-kong"
info_log.usecase = "use-case-1"
info_log.type = "info"
info_log.message = "processed document X"
write_custom_log("use-case-log", info_log)

error_log = custom_log_object()
error_log.location = "hong-kong"
error_log.usecase = "use-case-2"
error_log.type = "error"
error_log.message = "could not process document X"
write_custom_log("use-case-2-log", error_log)

write_log("this is what happened before the exception")

exception_handling_sample()

print("done")

# Notes
# App insights python SDK: https://github.com/Microsoft/ApplicationInsights-Python
#
# App insights isn't good for real time logging/debugging. There is usually a delay of 5 to 10 minutes
# before results appear in the portal. There can be a delay of up to an hour for custom events.