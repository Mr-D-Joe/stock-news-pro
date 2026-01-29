from datetime import datetime

class ThemeService:
    def __init__(self):
        pass

    def analyze_theme(self, query: str):
        """
        Mock implementation of thematic analysis.
        Returns deterministic ecosystems for predefined themes.
        """
        query_norm = query.lower().strip()
        
        # Mock Data for "Artificial Intelligence"
        if "ai" in query_norm or "künstliche intelligenz" in query_norm or "artificial" in query_norm:
            return {
                "theme": "Artificial Intelligence",
                "description": "Explosive growth sector driven by Generative AI and LLMs.",
                "winners": [
                    {"symbol": "NVDA", "name": "NVIDIA Corp", "reason": "GPU Monopoly"},
                    {"symbol": "MSFT", "name": "Microsoft", "reason": "OpenAI Stake"},
                    {"symbol": "PLTR", "name": "Palantir", "reason": "Enterprise AI"}
                ],
                "losers": [
                    {"symbol": "CHGG", "name": "Chegg", "reason": "Disrupted by ChatGPT"},
                    {"symbol": "FIVR", "name": "Fiverr", "reason": "AI Automation Risk"}
                ],
                "essay": "## The AI Revolution\n\nArtificial Intelligence is reshaping the global economy. Companies supplying the hardware (NVIDIA) and those integrating models into workflows (Microsoft) are positioned as primary beneficiaries.\n\nConversely, business models relying on simple information arbitrage or manual creative tasks face existential risks.",
                "generated_at": datetime.now().isoformat(),
                "is_mock": True
            }

        # Mock Data for "War" / "Defense"
        if "war" in query_norm or "krieg" in query_norm or "defense" in query_norm:
            return {
                "theme": "Global Conflict / Defense",
                "description": "Rising geopolitical tensions driving defense spending.",
                "winners": [
                    {"symbol": "RHM.DE", "name": "Rheinmetall", "reason": "Ammunition Demand"},
                    {"symbol": "LMT", "name": "Lockheed Martin", "reason": "Order Backlog"}
                ],
                "losers": [
                    {"symbol": "TUI.DE", "name": "TUI AG", "reason": "Geopolitical Uncertainty"},
                    {"symbol": "EZJ", "name": "EasyJet", "reason": "Fuel Costs & Airspace Risks"}
                ],
                "essay": "## Geopolitical Instability\n\nThe return of conventional warfare in Europe and the Middle East has triggered a massive rearmament cycle.\n\nDefense contractors with production capacity are structural winners, while travel and leisure sectors suffer from uncertainty and higher energy costs.",
                "generated_at": datetime.now().isoformat(),
                "is_mock": True
            }

        # Default Mock
        return {
            "theme": query,
            "description": f"Analysis for theme '{query}' (Mock).",
            "winners": [],
            "losers": [],
            "essay": f"## Analysis for {query}\n\nThis is a generated mock response for the requested theme. In a real implementation, this would trigger an LLM analysis of current news and market trends related to '{query}'.",
            "generated_at": datetime.now().isoformat(),
            "is_mock": True
        }
