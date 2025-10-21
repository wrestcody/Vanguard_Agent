import os
import json

# --- Secure API Handling ---

def get_api_key(service_name):
    """
    Retrieves an API key from an environment variable.

    Args:
        service_name (str): The name of the service (e.g., 'PRAETORIUM_NEXUS').

    Returns:
        str: The API key.

    Raises:
        ValueError: If the environment variable is not set.
    """
    api_key = os.environ.get(f"{service_name.upper()}_API_KEY")
    if not api_key:
        raise ValueError(f"API key for {service_name} not found in environment variables.")
    return api_key

def send_to_praetorium_nexus(enriched_payload):
    """
    Securely transmits the enriched JSON payload to the GRC-Copilot API endpoint.

    Args:
        enriched_payload (dict): The enriched risk data.

    Returns:
        bool: True if the transmission was successful, False otherwise.
    """
    print("--- Transmitting to Praetorium Nexus ---")

    # In a real implementation, this would be a secure HTTPS POST request.
    # api_key = get_api_key('PRAETORIUM_NEXUS')
    # headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    # response = requests.post(os.environ.get('PRAETORIUM_NEXUS_API_URL'), json=enriched_payload, headers=headers)

    print(f"Payload: {json.dumps(enriched_payload, indent=2)}")
    print("--- Transmission Complete (Mock) ---")

    # Mock response
    # return response.status_code == 200
    return True

# --- OPA Integration (Mock) ---

def get_risk_score_from_opa(cce_payload):
    """
    Applies a Rego policy to the CCE payload to determine a refined risk score.

    Args:
        cce_payload (dict): The Continuous Compliance Evidence payload.

    Returns:
        str: The refined risk score (e.g., 'Low', 'Medium', 'High', 'Critical').
    """
    print("--- Querying OPA for Risk Score ---")

    # In a real implementation, this would involve a call to an OPA server
    # or using the OPA Python library to evaluate the policy.

    # Mock logic based on the provided example:
    if cce_payload.get('severity') == 'High' and 'CUI/FedRAMP' in cce_payload.get('tags', []):
        refined_score = 'Critical'
    else:
        refined_score = cce_payload.get('severity', 'Low')

    print(f"Refined Score: {refined_score}")
    print("--- OPA Query Complete (Mock) ---")

    return refined_score

# --- LLM Integration (Mock) ---

def get_llm_summary(cce_payload):
    """
    Uses an LLM to generate a non-technical summary of the finding.

    Args:
        cce_payload (dict): The CCE payload.

    Returns:
        str: A non-technical summary.
    """
    print("--- Generating LLM Summary ---")

    # In a real implementation, this would involve a call to an LLM API
    # (e.g., GitHub Spark/Models or Copilot) with a carefully crafted prompt.
    # api_key = get_api_key('LLM_SERVICE')

    finding_description = cce_payload.get('description', 'No description provided.')

    # Mock LLM response:
    summary = f"This finding indicates a potential security weakness related to '{finding_description}'. "\
              "Immediate attention may be required to prevent unauthorized access or data exposure."

    print(f"Summary: {summary}")
    print("--- LLM Summary Generation Complete (Mock) ---")

    return summary

# --- Main Handler for Lambda ---

def lambda_handler(event, context):
    """
    The main entry point for the Lambda function.

    Args:
        event (dict): The CCE JSON payload from the KSI_Engine.
        context (object): The Lambda runtime context.

    Returns:
        dict: The enriched JSON payload.
    """
    print("--- Vanguard_Agent Processing Started ---")

    # 1. Receive and validate the CCE payload (validation omitted for brevity)
    cce_payload = event

    # 2. Apply policy-as-code for risk scoring
    refined_risk_score = get_risk_score_from_opa(cce_payload)

    # 3. Use LLM for summarization
    executive_summary = get_llm_summary(cce_payload)

    # 4. Construct the enriched payload
    enriched_payload = {
        'cce_finding_id': cce_payload.get('id'),
        'original_severity': cce_payload.get('severity'),
        'refined_risk_score': refined_risk_score,
        'executive_summary': executive_summary,
        'remediation_playbook': 's3_public_access_fix.tf', # Example playbook
        'original_payload': cce_payload
    }

    # 5. Transmit the enriched payload to the Praetorium_Nexus
    send_to_praetorium_nexus(enriched_payload)

    print("--- Vanguard_Agent Processing Complete ---")

    return enriched_payload

# --- Example Usage (for local testing) ---

if __name__ == '__main__':
    # Mock CCE payload from KSI_Engine
    mock_cce_payload = {
        'id': 'CCE-2023-12345',
        'finding_type': 'NIST-CM-6',
        'severity': 'High',
        'asset_id': 'arn:aws:s3:::sensitive-data-bucket',
        'description': 'S3 bucket has public read access.',
        'tags': ['CUI/FedRAMP', 'Production']
    }

    lambda_handler(mock_cce_payload, None)
