import React from "react";
import { LiveKitRoom } from "./LiveKitRoom";

interface LiveKitProviderProps {
  children: React.ReactNode;
  token: string;
  url: string;
  onConnected?: () => void;
  onDisconnected?: () => void;
}

export function LiveKitProvider({
  children,
  token,
  url,
  onConnected,
  onDisconnected,
}: LiveKitProviderProps) {
  return (
    <LiveKitRoom
      token={token}
      serverUrl={url}
      connect={true}
      onConnected={onConnected}
      onDisconnected={onDisconnected}
    >
      {children}
    </LiveKitRoom>
  );
}
