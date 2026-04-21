import re
import spacy

nlp = spacy.load("en_core_web_sm")

#spacy
def spacy_intent_extraction(user_input):
    user_input = user_input.lower()
    
    #GREETINGS
    if re.search(r'\b(hi|hello|hey|good morning|good evening|yo)\b', user_input.lower()):
        return "greeting"

    
    #EXIT
    elif any(exit_word in user_input for exit_word in ["bye", "exit","quit","goodbye"]):
        return "exit"
    
   #CHECK-IN
    # View all check-ins
    elif ("show" in user_input or "view" in user_input) and "checkins" in user_input:
        return "view_all_checkins"

    # Get check-in status (specific passenger)
    elif "check-in status" in user_input or "checkin status" in user_input:
        return "get_checkin_status"

    # Perform check-in (exact match to avoid false triggers)
    elif any(phrase in user_input for phrase in ["perform check in", "add check in"]) or "check in" in user_input.split():
        return "check_in"
    
    elif "update check-in" in user_input or "change check-in" in user_input:
        return "update_checkin_status"


    
   #SECURITY CHECK
    elif "security" in user_input and ("check" in user_input or "clearance" in user_input):
        return "security_check"
    elif "view" in user_input and ("security" in user_input and ("status" in user_input or "statuses" in user_input)):
        return "view_all_security_status"
    elif "update" in user_input and "security" in user_input:
        return "update_security_status"
    elif "security" in user_input and ("status" in user_input or "get" in user_input):
        return "get_security_status"

    

    
    #BAGGAGE 
    elif "baggage" in user_input or "luggage" in user_input:
        return "baggage_info"
    
   #UPDATE
    elif "update" in user_input and "email" in user_input:
        return "update_email"
    elif "update" in user_input and "phone" in user_input:
        return "update_phone"
    elif "update" in user_input and "name" in user_input:
        return "update_name"
    
    #PASSENGER FUNCTIONS
    elif ("add" in user_input and "passenger" in user_input) or ("register" in user_input and "passenger" in user_input):
        return "add_passenger"
    elif any(word in user_input for word in ["view", "see", "show", "display", "find", "get", "details", "info"]) and (
    "passenger" in user_input or "person" in user_input or "details" in user_input):
        return "view_passenger"
    elif any(word in user_input for word in ["delete", "remove", "bump", "drop"]) and "passenger" in user_input:
        return "delete_passenger"

    #FLIGHT
    elif any(word in user_input.lower() for word in ["flights to", "flight to", "show me flights to",]):
        return "get_flight_by_destination"
    elif any(phrase in user_input.lower() for phrase in ["show all flights", "show me all flights","display flights","list all flights","show the available flights"]):
        return "get_all_flights"
    elif "flight number" in user_input.lower() or "track flight" in user_input.lower() or "flight status" in user_input.lower():
        return "get_flight_by_number"
    elif any(word in user_input.lower() for word in ["from", "leaving from", "departing from"]):
        return "get_flight_by_departure"
    elif ("check" in user_input and "flights" in user_input) or ("flight" in user_input and "status" in user_input):
        return "check_flight_status"
    elif "flight" in user_input.lower() and any(verb in user_input.lower() for verb in ["add", "register", "insert", "create", "schedule"]):
        return "add_flight"
    elif any(kw in user_input.lower() for kw in ["update flight", "edit flight", "change flight", "modify flight", "want to update"]):
        return "update_flight"
    elif any(kw in user_input for kw in ["delete flight", "remove flight", "cancel flight", "drop flight"]):
        return "delete_flight"


   
    else:
        return "fallback_unknown"
    
def extract_passenger_info(user_input):
    doc = nlp(user_input)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    number_match = re.search(r'\b(\d+)\b', user_input)
    number = int(number_match.group(1)) if number_match else None
    return names, number

def extract_flight_number(user_input):
    match = re.search(r'\b([A-Z]{2}\d{2,4})\b', user_input.upper())
    if match:
        return match.group(1)
    return None