export function LangGraphLogoSVG({
  className,
  width,
  height,
}: {
  width?: number;
  height?: number;
  className?: string;
}) {
  return (
    <img
      src="/logo.png"
      alt="自驱 · 通用智能体"
      width={width}
      height={height}
      className={`object-contain flex-shrink-0 ${className ?? ""}`}
    />
  );
}
