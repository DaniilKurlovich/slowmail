import styled from 'styled-components';

export const Flex = styled.div`
    display: flex;
    ${(props) => (props.height ? `height: ${props.height}` : '')};
    ${(props) => (props.width ? `width: ${props.width}` : '')};
    ${(props) => (props.maxHeight ? `max-height: ${props.maxHeight}` : '')};
    ${(props) => (props.maxWidth ? `max-width: ${props.maxWidth}` : '')};
    ${(props) => (props.minHeight ? `min-height: ${props.minHeight}` : '')};
    ${(props) => (props.minWidth ? `min-width: ${props.minWidth}` : '')};
    ${(props) => (props.margin ? `margin: ${props.margin}` : '')};
    ${(props) => (props.padding ? `padding: ${props.padding}` : '')};
    ${(props) => (props.column ? 'flex-direction: column' : '')};
    ${(props) => (props.justifyContentCenter ? 'justify-content: center' : '')};
    ${(props) => (props.justifyContentBetween ? 'justify-content: space-between' : '')};
    ${(props) => (props.justifyContentAround ? 'justify-content: space-around' : '')};
    ${(props) => (props.justifyContentEvenly ? 'justify-content: space-evenly' : '')};
    ${(props) => (props.alignContentCenter ? 'align-content: center' : '')};
    ${(props) => (props.alignContentStart ? 'align-content: flex-start' : '')};
    ${(props) => (props.alignContentEnd ? 'align-content: flex-end' : '')};
    ${(props) => (props.alignItemsCenter ? 'align-items: center' : '')};
    ${(props) => (props.alignItemsBaseline ? 'align-items: baseline' : '')};
    ${(props) => (props.alignItemsStart ? 'align-items: flex-start' : '')};
    ${(props) => (props.alignItemsEnd ? 'align-items: flex-end' : '')};
    ${(props) => (props.borderBox ? 'box-sizing: border-box' : '')};
    ${(props) => (props.flexFlowWrap ? 'flex-flow: wrap' : '')};
    z-index: 100;
`;
