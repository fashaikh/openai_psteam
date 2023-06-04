import { Example } from "./Example";

import styles from "./Example.module.css";

export type ExampleModel = {
    text: string;
    value: string;
};

const EXAMPLES: ExampleModel[] = [
    {
        text: "Load the grounding prompt",
        value: "You are an AI assistant who helps answer questions on scientific publications. \
        Use the knowledge from Google Scholar https://scholar.google.com/citations?view_op=list_works&hl=en&hl=en&tzom=300&user=elEQEEEAAAAJ \
        to answer the questions."
    },
    { text: "Can you desribe the OSATS scoring?", value: "Can you describe the OSATS scoring?"},
    { text: "Can you provide steps for motion texture analysis?", value: "Can you provide steps for motion texture analysis?" }
];

interface Props {
    onExampleClicked: (value: string) => void;
}

export const ExampleList = ({ onExampleClicked }: Props) => {
    return (
        <ul className={styles.examplesNavList}>
            {EXAMPLES.map((x, i) => (
                <li key={i}>
                    <Example text={x.text} value={x.value} onClick={onExampleClicked} />
                </li>
            ))}
        </ul>
    );
};
