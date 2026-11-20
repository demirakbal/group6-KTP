# Café Shift Advisor

## Chosen topic

Our system will model how a café owner makes daily operational decisions and help shift leads decide what to do next. It will provide rule-based advice about staff allocation, task priorities, food and dessert preparation, and stock replenishment, considering menu quantities, pending orders, staff skills, preparation times, and ingredient availability.

For example, it could help decide whether to start making another cake when one slice remains or wait until it sells out. Using forward chaining, rules could infer that another batch is needed, check whether ingredients, staff, and enough time before closing are available, and then recommend starting preparation. The system will explain the reasoning behind its advice. These example rules will be refined and validated through the expert interview.

## Chosen expert

Our chosen expert is **Murat, the owner of People of Coffee, a café in Groningen**. We will interview him about how he manages daily café operations and use his knowledge to develop and validate the system's rules and recommendations.

See our [expert interview questionnaire](expert-interview.md) for the planned questions.

## Running the prototype

Requires Python 3. Run from the repository folder:

```sh
python3 main.py
```

Enter the number of slices remaining, preparation time in minutes, and minutes until closing, and answer yes/no questions about demand, ingredients, and staff availability. The prototype prints a recommendation and the rules used to reach it.

The eleven illustrative rules are stored in [knowledge_base.json](knowledge_base.json), separately from the forward-chaining engine in [main.py](main.py). They have not yet been validated by Murat. This first prototype covers cake preparation only; broader shift and ordering decisions will follow the expert interview. 