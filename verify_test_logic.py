
import random

# Mock Data
concepts = [
    {'id': 'symmetry_concept', 'name': 'Symmetry', 'def': 'Symmetry is when a shape or picture can be split into two parts that look exactly the same — like a mirror image.', 'props': ['Example: Heart', 'Example: Butterfly', 'Example: Square']},
    {'id': 'right_angle_concept', 'name': 'Right Angle', 'def': 'A Right Angle is an angle of exactly 90 degrees, like the corner of a square.', 'props': ['Symbol: A small square in the corner.']},
    {'id': 'parallel_concept', 'name': 'Parallel Lines', 'def': 'Parallel lines are lines that never touch, no matter how far they go. Like train tracks.', 'props': ['Symbol: Arrows on the lines.']}
]

shapes = [
    {'id': 'triangle', 'name': 'Triangle', 'category': '2d', 'def': 'A shape with 3 sides and 3 vertices.', 'props': ['Sides: 3', 'Vertices: 3']},
    {'id': 'square', 'name': 'Square', 'category': '2d', 'isQuad': True, 'def': '4 equal sides and 4 right angles.', 'props': ['Sides: 4', 'Vertices: 4', 'Parallel Sides: 2 pairs']},
    {'id': 'rectangle', 'name': 'Rectangle', 'category': '2d', 'isQuad': True, 'def': '4 sides, opposite sides equal.', 'props': ['Sides: 4', 'Vertices: 4', 'Parallel Sides: 2 pairs']},
    {'id': 'parallelogram', 'name': 'Parallelogram', 'category': '2d', 'isQuad': True, 'def': 'A quadrilateral with two pairs of parallel sides.', 'props': ['Sides: 4', 'Vertices: 4', 'Opposite sides parallel']},
    {'id': 'rhombus', 'name': 'Rhombus', 'category': '2d', 'isQuad': True, 'def': 'A quadrilateral with all four sides equal in length.', 'props': ['Sides: 4', 'Vertices: 4', 'All sides equal']},
    {'id': 'trapezoid', 'name': 'Trapezoid', 'category': '2d', 'isQuad': True, 'def': 'A quadrilateral with at least one pair of parallel sides.', 'props': ['Sides: 4', 'Vertices: 4', 'One Pair of Parallel Sides']},
    {'id': 'pentagon', 'name': 'Pentagon', 'category': '2d', 'def': 'A polygon with 5 sides.', 'props': ['Sides: 5', 'Vertices: 5']},
    {'id': 'hexagon', 'name': 'Hexagon', 'category': '2d', 'def': 'A polygon with 6 sides.', 'props': ['Sides: 6', 'Vertices: 6']},
    {'id': 'octagon', 'name': 'Octagon', 'category': '2d', 'def': 'A polygon with 8 sides.', 'props': ['Sides: 8', 'Vertices: 8']},
    {'id': 'star', 'name': 'Star', 'category': '2d', 'def': 'A pointed shape, typically with 5 or more points.', 'props': ['5 Points (usually)', '10 Sides']},
    {'id': 'circle', 'name': 'Circle', 'category': '2d', 'def': 'A round shape with no corners.', 'props': ['Sides: 0', 'Vertices: 0']},
    {'id': 'oval', 'name': 'Oval', 'category': '2d', 'def': 'A stretched circle, like an egg.', 'props': ['Sides: 0', 'Vertices: 0']},
    {'id': 'cube', 'name': 'Cube', 'category': '3d', 'def': 'A 3D shape with 6 square faces.', 'props': ['Faces: 6', 'Edges: 12', 'Vertices: 8']},
    {'id': 'cylinder', 'name': 'Cylinder', 'category': '3d', 'def': 'A 3D shape with 2 circular bases.', 'props': ['Faces: 2 (flat circles)', '1 curved surface']},
    {'id': 'rectangular_prism', 'name': 'Rectangular Prism', 'category': '3d', 'def': 'A 3D shape like a brick or cereal box.', 'props': ['Faces: 6', 'Edges: 12', 'Vertices: 8']},
    {'id': 'hexagonal_prism', 'name': 'Hexagonal Prism', 'category': '3d', 'def': 'A 3D prism with hexagonal bases.', 'props': ['Faces: 8', 'Edges: 18', 'Vertices: 12']},
    {'id': 'cone', 'name': 'Cone', 'category': '3d', 'def': 'A 3D shape with a circular base and a point at the top.', 'props': ['1 curved surface', '1 flat circle']},
    {'id': 'pyramid', 'name': 'Square Pyramid', 'category': '3d', 'def': 'A 3D shape with a square base and triangle sides.', 'props': ['Faces: 5', 'Edges: 8', 'Vertices: 5']},
    {'id': 'sphere', 'name': 'Sphere', 'category': '3d', 'def': 'A perfectly round 3D shape, like a ball.', 'props': ['Faces: 0', 'Edges: 0', 'Vertices: 0']}
]

all_items = shapes + concepts

def get_options(correct_item, all_items_list, count=4):
    pool = [i for i in all_items_list if i['id'] != correct_item['id']]
    # Filter to same category if possible (simple heuristic)
    same_cat = [i for i in pool if i.get('category') == correct_item.get('category')]
    if len(same_cat) >= count - 1:
        pool = same_cat
    
    random.shuffle(pool)
    return pool[:count-1]

def generate_question(q_type):
    # 0: Shape Identification (Image -> Name)
    # 1: Definition Matching (Def -> Name)
    # 2: Property Matching (Name -> Props)
    # 3: Inverse Property (Prop -> Name)
    # 5: Concept Match (Concept Def -> Name)
    
    # Types 0, 1, 5 are mostly Name matching, fairly safe if definitions are unique.
    # Type 2: Which properties belong to [Shape]? (Multi-choice options are sets of props)
    # Type 3: Which shape has [Property]? (Target: Shape Name. Options: Shape Names)
    
    if q_type == 3:
        result = generate_question_type_3(shapes)
        if result is None:
            return None
        
        question_text, correct_answer_name, options_names, prop_str = result

        # Determine all correct matches among the generated options
        correct_matches = []
        for opt_name in options_names:
            # Find the shape object for this option name
            shape_obj = next((s for s in shapes if s['name'] == opt_name), None)
            if shape_obj and 'props' in shape_obj:
               # prop_str is e.g. "Sides: 4"
               # We check if shape_obj has this property
               if prop_str in shape_obj['props']:
                   correct_matches.append(opt_name)
        
        # The original code had an incorrect `if len(correct_matches) > 1:` block here.
        # The final return structure for q_type 3 already handles `is_ambiguous`.
        # We need `prop` and `target` from the `generate_question_type_3` result,
        # which are not directly available from `question_text, correct_answer_name, options_names, prop_str`.
        # For this fix, we'll assume `prop` and `target` are part of the `result` or derived.
        # Since the instruction only focuses on `correct_matches` logic,
        # and the original code had `prop` and `target` in the final return,
        # we'll assume they are available in the scope where this `return` statement is.
        # For a complete fix, `generate_question_type_3` would need to return more.
        # For now, we'll use placeholders or assume they exist.
        
        # Placeholder for `prop` and `target` if not returned by `generate_question_type_3`
        # In a real scenario, `generate_question_type_3` should return the full question object or its components.
        # For the purpose of this edit, we'll assume `prop` and `target` are available from `result` or parent scope.
        # The original code had `prop` and `target` in the final return, so we'll keep that structure.
        # Let's assume `generate_question_type_3` returns `(question_text, correct_answer_name, options_names, prop_str, target_obj, prop_value)`
        # For this specific edit, we'll use `prop_str` as `prop` and `correct_answer_name` as `target['name']`
        
        return {
            'type': 3,
            'question': question_text, # f"Which shape has: {prop_str}?"
            'target': correct_answer_name, # This is the name of the correct shape
            'options': options_names,
            'prop': prop_str, # The property string used in the question
            'correct_matches': correct_matches,
            'is_ambiguous': len(correct_matches) > 1
        }
    return None

# Placeholder for generate_question_type_3 to make the code runnable for testing the fix
def generate_question_type_3(shapes_list):
    """
    Simulates generating a Type 3 question (Inverse Property) with VALIDATION.
    "Which shape has X?"
    Returns: (question_text, correct_answer_name, options_names, prop_str)
    """
    target = random.choice(shapes_list)
    if not target.get('props'):
        return None  # Skip if no props
        
    prop_str = target['props'][0] # e.g. "Sides: 4"
    if ': ' not in prop_str:
        return None
        
    key, val = prop_str.split(': ')
    
    question_text = f"Which shape has {key}: {val}?"
    correct_answer = target['name']
    
    # NEW LOGIC: Validation of distractors matches JS implementation
    options = [correct_answer]
    # Try to find 3 valid distractors
    attempts = 0
    while len(options) < 4 and attempts < 200:
        candidate = random.choice(shapes_list)
        
        # Check if candidate has the property
        has_prop = False
        if candidate.get('props'):
            # In JS we did: r.props.some(p => p.startsWith(key + ':') && p.includes(val))
            # Here we check if prop_str matches or is contained
            for p in candidate['props']:
                if p == prop_str:
                    has_prop = True
                    break
        
        if (candidate['id'] != target['id'] and 
            candidate['name'] not in options and 
            not has_prop):
            options.append(candidate['name'])
        
        attempts += 1
            
    # Fallback (same as JS check)
    while len(options) < 4:
         candidate = random.choice(shapes_list)
         if candidate['name'] not in options:
             options.append(candidate['name'])
    
    random.shuffle(options)
    return (question_text, correct_answer, options, prop_str)


def run_simulation(iterations=1000):
    ambiguous_count = 0
    issues = []
    
    for _ in range(iterations):
        q = generate_question(3)
        if q and q['is_ambiguous']:
            ambiguous_count += 1
            issues.append(q)
            
    print(f"Simulation of Type 3 (Inverse Property) Questions")
    print(f"Iterations: {iterations}")
    print(f"Ambiguous Questions Found: {ambiguous_count}")
    
    if issues:
        print("\nExamples of Ambiguity:")
        for i in range(min(5, len(issues))):
            print(f"Q: {issues[i]['question']}")
            print(f"Target logic intended: {issues[i]['target']}")
            print(f"All valid answers in options: {issues[i]['correct_matches']}")
            print("-" * 20)

if __name__ == '__main__':
    run_simulation()
