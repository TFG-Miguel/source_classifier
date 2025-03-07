from re import findall, IGNORECASE
from utils import load_json, get_domain, get_mime_type, get_text

class Verifier:
    """
    A class to verify URLs against predefined rules such as:
    - Forbidden domains
    - Allowed MIME types
    - Multiple mentions of specific patterns in text content
    """

    def __init__(self, rules_file: str):
        """
        Initializes the Verifier with rules from a JSON file.

        Args:
            rules_file (str): The path to the JSON file containing rules.

        Raises:
            Exception: If there is an issue loading the rules file.
        """
        rules = load_json(rules_file)
        self.__forbidden_domains = rules['forbidden-domains']
        self.__allowed_mime_types = rules['allowed-mime-types']
        self.__multiples_mentions_target = rules['multiples-mentions']
            

    def __check_forbidden_domains(self, url: str) -> str:
        """
        Checks if a URL belongs to a forbidden domain.

        Args:
            url (str): The URL to check.

        Returns:
            str: A message indicating if the domain is forbidden, or None if allowed.

        Example:
            reason = verifier.__check_forbidden_domains("https://example.com")
        """
        prefix = "FORBIDDEN DOMAIN"
        domain = get_domain(url)
        for reason, domains in self.__forbidden_domains.items():
            for d in domains:
                if d in domain:
                    return f"{prefix} {reason} {domain}"

    def __check_allowed_mime_type(self, url: str) -> str:
        """
        Checks if the MIME type of the URL is allowed.

        Args:
            url (str): The URL to check.

        Returns:
            str: MIME type if allowed, otherwise an error message.

        Example:
            mime_type = verifier.__check_allowed_mime_type("https://example.com/file.pdf")
        """
        mime_type = get_mime_type(url)
        if not mime_type:
            return "UNKNOWN MIME TYPE"
        if mime_type not in self.__allowed_mime_types:
            return f"NOT ALLOWED MIME TYPE : {mime_type}"
        return mime_type

    def __check_multiples_mentions(self, url: str) -> str:
        """
        Checks if a specified pattern appears more than the allowed limit in the page content.

        Args:
            url (str): The URL of the page.

        Returns:
            str: A message indicating excessive occurrences, or None if within limits.

        Example:
            mention_check = verifier.__check_multiples_mentions("https://example.com")
        """
        mime_type = self.__check_allowed_mime_type(url)
        if "MIME TYPE" in mime_type:
            return mime_type
        if mime_type != "text/type":
            return
        
        text = get_text(url)
        regex = self.__multiples_mentions_target['regex']
        limit = self.__multiples_mentions_target['limit']
        matches = findall(regex, text, IGNORECASE)

        if matches >= limit:
            return f"MULTIPLE MENTIONS OF r'{regex}': {matches}"

    def verify(self, url: str) -> str:
        """
        Verifies a URL against all rules.

        Args:
            url (str): The URL to check.

        Returns:
            str: The first rule violation message found, or None if all checks pass.

        Example:
            result = verifier.verify("https://example.com")
        """
        rules_methods = [
            self.__check_forbidden_domains,
            self.__check_multiples_mentions
        ]

        for rule in rules_methods:
            reason = rule(url)
            if reason:
                return reason
